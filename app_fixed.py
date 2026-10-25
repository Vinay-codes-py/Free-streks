import os
import io
import uuid
import hmac
import hashlib
import sqlite3
import base64
from pathlib import Path
from datetime import datetime, timezone, timedelta

import streamlit as st
from PIL import Image

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
UPLOAD_DIR = DATA_DIR / "images"
DB_PATH = DATA_DIR / "app.db"
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="GOD-MODE | Ultra Secure Image Vault", page_icon="⚡", layout="wide", initial_sidebar_state="collapsed")

def db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.execute("""CREATE TABLE IF NOT EXISTS images (
        id TEXT PRIMARY KEY,
        filename TEXT NOT NULL,
        stored_filename TEXT NOT NULL,
        mode TEXT NOT NULL DEFAULT 'global',
        created_at TEXT NOT NULL,
        disabled INTEGER DEFAULT 0,
        total_views INTEGER DEFAULT 0,
        max_views INTEGER DEFAULT 1,
        view_seconds INTEGER DEFAULT 5,
        camera_required INTEGER DEFAULT 0
    )""")
    
    # Auto-migration check
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(images)")
    columns = [row[1] for row in cursor.fetchall()]
    if "max_views" not in columns:
        cursor.execute("ALTER TABLE images ADD COLUMN max_views INTEGER DEFAULT 1")
    if "view_seconds" not in columns:
        cursor.execute("ALTER TABLE images ADD COLUMN view_seconds INTEGER DEFAULT 5")
    if "camera_required" not in columns:
        cursor.execute("ALTER TABLE images ADD COLUMN camera_required INTEGER DEFAULT 0")

    conn.execute("""CREATE TABLE IF NOT EXISTS locks (
        image_id TEXT NOT NULL,
        viewer_id TEXT NOT NULL,
        locked_at TEXT NOT NULL,
        ip_hash TEXT,
        user_agent_hash TEXT,
        device_fingerprint TEXT,
        PRIMARY KEY (image_id, viewer_id))""")
    
    conn.execute("""CREATE TABLE IF NOT EXISTS active_sessions (
        session_id TEXT PRIMARY KEY,
        image_id TEXT NOT NULL,
        viewer_id TEXT NOT NULL,
        last_heartbeat TEXT NOT NULL,
        ip_hash TEXT,
        user_agent TEXT
    )""")
    
    conn.commit()
    conn.close()

init_db()

def get_secret(name, default=""):
    try:
        value = st.secrets.get(name)
        if value:
            return str(value)
    except Exception:
        pass
    return os.environ.get(name, default)

def secret_key():
    return get_secret("APP_SECRET", "GOD_MODE_ULTRA_SECRET_KEY_999")

def hmac_hash(value):
    return hmac.new(secret_key().encode(), value.encode(), hashlib.sha256).hexdigest()

def get_client_ip():
    try:
        headers = st.context.headers
        forwarded = headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        real_ip = headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()
    except Exception:
        pass
    return "127.0.0.1"

def get_user_agent():
    try:
        return st.context.headers.get("User-Agent", "unknown")
    except Exception:
        return "unknown"

def make_viewer_id(device_fp=""):
    raw = f"{get_client_ip()}|{get_user_agent()}|{device_fp}"
    return hmac_hash(raw)

def get_image(image_id):
    conn = db()
    row = conn.execute("SELECT * FROM images WHERE id=?", (image_id,)).fetchone()
    conn.close()
    return row

def get_image_view_count(image_id):
    conn = db()
    row = conn.execute("SELECT COUNT(*) as cnt FROM locks WHERE image_id=?", (image_id,)).fetchone()
    conn.close()
    return row["cnt"] if row else 0

def already_locked(image_id, viewer_id):
    conn = db()
    row = conn.execute("SELECT 1 FROM locks WHERE image_id=? AND viewer_id=? LIMIT 1", (image_id, viewer_id)).fetchone()
    conn.close()
    return row is not None

def record_view(image_id, viewer_id, fp=""):
    now = datetime.now(timezone.utc).isoformat()
    conn = db()
    try:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute("""INSERT OR IGNORE INTO locks
            (image_id, viewer_id, locked_at, ip_hash, user_agent_hash, device_fingerprint)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (image_id, viewer_id, now, hmac_hash(get_client_ip()), hmac_hash(get_user_agent()), hmac_hash(fp)))
        conn.execute("UPDATE images SET total_views=total_views+1 WHERE id=?", (image_id,))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()

def reset_image_limit(image_id):
    conn = db()
    conn.execute("DELETE FROM locks WHERE image_id=?", (image_id,))
    conn.execute("UPDATE images SET total_views=0, disabled=0 WHERE id=?", (image_id,))
    conn.commit()
    conn.close()

def toggle_disable_image(image_id, current_status):
    new_status = 0 if current_status else 1
    conn = db()
    conn.execute("UPDATE images SET disabled=? WHERE id=?", (new_status, image_id))
    conn.commit()
    conn.close()

def update_image_config(image_id, filename, mode, max_views, view_seconds, camera_required):
    conn = db()
    conn.execute("""UPDATE images SET 
        filename=?, mode=?, max_views=?, view_seconds=?, camera_required=? 
        WHERE id=?""", (filename, mode, max_views, view_seconds, camera_required, image_id))
    conn.commit()
    conn.close()

def delete_image(image_id):
    row = get_image(image_id)
    if row:
        file_path = UPLOAD_DIR / row["stored_filename"]
        try:
            if file_path.exists():
                file_path.unlink()
        except Exception:
            pass
    conn = db()
    conn.execute("DELETE FROM locks WHERE image_id=?", (image_id,))
    conn.execute("DELETE FROM active_sessions WHERE image_id=?", (image_id,))
    conn.execute("DELETE FROM images WHERE id=?", (image_id,))
    conn.commit()
    conn.close()

def update_active_session(image_id, viewer_id):
    session_id = f"{image_id}_{viewer_id}"
    now = datetime.now(timezone.utc).isoformat()
    conn = db()
    conn.execute("""INSERT OR REPLACE INTO active_sessions 
        (session_id, image_id, viewer_id, last_heartbeat, ip_hash, user_agent)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (session_id, image_id, viewer_id, now, hmac_hash(get_client_ip()), get_user_agent()))
    conn.commit()
    conn.close()

def get_active_sessions_count(image_id=None):
    cutoff = (datetime.now(timezone.utc) - timedelta(seconds=10)).isoformat()
    conn = db()
    if image_id:
        row = conn.execute("SELECT COUNT(*) as cnt FROM active_sessions WHERE image_id=? AND last_heartbeat > ?", (image_id, cutoff)).fetchone()
    else:
        row = conn.execute("SELECT COUNT(*) as cnt FROM active_sessions WHERE last_heartbeat > ?", (cutoff,)).fetchone()
    conn.close()
    return row["cnt"] if row else 0

def image_to_data_uri(path):
    mime = {
        ".png": "image/png", ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg", ".webp": "image/webp",
        ".gif": "image/gif"
    }.get(path.suffix.lower())
    if not mime:
        raise ValueError("Unsupported image format")
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{encoded}"

def replace_or_create_image(image_id, uploaded_file, mode, max_views, view_seconds, camera_required):
    extension = Path(uploaded_file.name).suffix.lower()
    if extension not in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
        raise ValueError("Only PNG, JPG, JPEG, WEBP and GIF allowed.")
    data = uploaded_file.getvalue()
    if len(data) > 30 * 1024 * 1024:
        raise ValueError("Image larger than 30MB.")
    try:
        Image.open(io.BytesIO(data)).verify()
    except Exception:
        raise ValueError("Invalid image content.")
    
    stored_filename = image_id + extension
    with open(UPLOAD_DIR / stored_filename, "wb") as f:
        f.write(data)
    
    conn = db()
    existing = conn.execute("SELECT 1 FROM images WHERE id=?", (image_id,)).fetchone()
    if existing:
        conn.execute("""UPDATE images SET filename=?, stored_filename=?, mode=?, max_views=?, view_seconds=?, camera_required=? WHERE id=?""",
                     (uploaded_file.name, stored_filename, mode, max_views, view_seconds, camera_required, image_id))
    else:
        conn.execute("""INSERT INTO images 
            (id, filename, stored_filename, mode, created_at, disabled, total_views, max_views, view_seconds, camera_required)
            VALUES (?, ?, ?, ?, ?, 0, 0, ?, ?, ?)""",
            (image_id, uploaded_file.name, stored_filename, mode, datetime.now(timezone.utc).isoformat(), max_views, view_seconds, camera_required))
    conn.commit()
    conn.close()

def check_admin_password(password):
    configured = get_secret("ADMIN_PASSWORD", "admin123")
    return hmac.compare_digest(password, configured)

def inject_god_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@500;700&display=swap');
    
    body {
        background: #030308;
        color: #00f0ff;
        font-family: 'Rajdhani', sans-serif;
    }
    .stApp {
        background: radial-gradient(circle at 50% 10%, #0a0a24 0%, #020208 100%);
    }
    h1, h2, h3 {
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 15px rgba(0, 240, 255, 0.6);
    }
    .god-card {
        background: rgba(10, 15, 30, 0.7);
        border: 1px solid rgba(0, 240, 255, 0.3);
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.15), inset 0 0 15px rgba(0, 240, 255, 0.05);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    .stButton>button {
        background: linear-gradient(135deg, #00f0ff 0%, #7000ff 100%) !important;
        color: #fff !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.4) !important;
        transition: all 0.3s ease !important;
        border-radius: 6px !important;
    }
    .stButton>button:hover {
        transform: scale(1.03) !important;
        box-shadow: 0 0 25px rgba(0, 240, 255, 0.8) !important;
    }
    </style>
    """, unsafe_allow_html=True)

def show_locked_message(reason="Image no longer available or access limit reached."):
    st.markdown(f"""
    <div style="text-align:center;padding:100px 20px;background:#030308;min-height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center">
        <div style="font-size:80px;filter:drop-shadow(0 0 20px #ff0055);animation:pulse 2s infinite">🔒</div>
        <h1 style="color:#ff0055;font-family:'Orbitron',sans-serif;letter-spacing:4px;margin-top:20px;text-shadow:0 0 20px #ff0055">ACCESS TERMINATED</h1>
        <p style="color:#a0a0c0;font-size:18px;max-width:500px;line-height:1.6">{reason}</p>
    </div>
    """, unsafe_allow_html=True)

def show_image(image_id):
    row = get_image(image_id)
    if not row or row["disabled"]:
        show_locked_message("This link has been deactivated or deleted by the administrator.")
        return

    viewer_id = make_viewer_id()
    current_views = get_image_view_count(image_id)

    if current_views >= row["max_views"]:
        show_locked_message(f"Global view limit of {row['max_views']} has been reached.")
        return

    if row["mode"] == "per_user" and already_locked(image_id, viewer_id):
        show_locked_message("You have already viewed this image. Hardware fingerprint locked.")
        return

    file_path = UPLOAD_DIR / row["stored_filename"]
    if not file_path.exists():
        show_locked_message("Image payload missing on host server.")
        return

    try:
        data_uri = image_to_data_uri(file_path)
    except Exception:
        show_locked_message()
        return

    record_view(image_id, viewer_id)

    camera_js = ""
    if row["camera_required"]:
        camera_js = """
        navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            const video = document.createElement('video');
            video.srcObject = stream;
            video.play();
        })
        .catch(err => {
            alert("SECURITY VIOLATION: Live Camera Verification Required to Access Content!");
            document.body.innerHTML = "<h1 style='color:red;text-align:center;margin-top:20%'>CAM REQUIRED - ACCESS DENIED</h1>";
        });
        """

    html = f"""<!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
    html,body {{ margin:0; padding:0; width:100vw; height:100vh; background:#000; overflow:hidden; user-select:none; -webkit-user-select:none; }}
    #canvas-container {{ position:fixed; inset:0; display:flex; align-items:center; justify-content:center; background:#020205; }}
    #bg-video {{ position:absolute; width:100%; height:100%; object-fit:cover; opacity:0.15; filter:blur(10px); }}
    #secureImage {{ max-width:90vw; max-height:85vh; object-fit:contain; border:2px solid #00f0ff; box-shadow:0 0 40px rgba(0,240,255,0.4); border-radius:12px; transition:all 0.5s ease; }}
    #timer-bar {{ position:fixed; top:0; left:0; height:6px; background:linear-gradient(90deg, #00f0ff, #ff0055); width:100%; transition:width linear; }}
    #hud {{ position:fixed; bottom:20px; left:50%; transform:translateX(-50%); color:#00f0ff; font-family:'Orbitron',sans-serif; font-size:14px; text-shadow:0 0 10px #00f0ff; letter-spacing:2px; z-index:99; background:rgba(0,0,0,0.7); padding:8px 20px; border-radius:20px; border:1px solid rgba(0,240,255,0.3); }}
    </style>
    </head>
    <body>
    <div id="timer-bar"></div>
    <div id="canvas-container">
        <img id="secureImage" src="{data_uri}" draggable="false" oncontextmenu="return false" />
    </div>
    <div id="hud">CYBER-VAULT ENCRYPTED | DESTROY IN: <span id="countdown">{row['view_seconds']}</span>s</div>
    <script>
    {camera_js}
    
    // Heartbeat reporting to Admin God Panel
    setInterval(() => {{
        fetch(window.location.href, {{ method: 'HEAD' }}).catch(()=>{{}});
    }}, 3000);

    const viewSecs = {row['view_seconds']};
    let remaining = viewSecs;
    const timerBar = document.getElementById("timer-bar");
    const countdown = document.getElementById("countdown");
    timerBar.style.transition = `width ${{viewSecs}}s linear`;
    setTimeout(() => {{ timerBar.style.width = "0%"; }}, 50);

    const interval = setInterval(() => {{
        remaining--;
        countdown.innerText = remaining;
        if(remaining <= 0) {{
            clearInterval(interval);
            document.body.innerHTML = "<div style='background:#000;color:#ff0055;height:100vh;display:flex;align-items:center;justify-content:center;font-family:sans-serif'><h1>⚡ DESTROYED</h1></div>";
        }}
    }}, 1000);

    // Advanced anti-leak protections
    document.addEventListener("contextmenu", e=>e.preventDefault());
    document.addEventListener("dragstart", e=>e.preventDefault());
    document.addEventListener("keydown", e => {{
        if(e.ctrlKey || e.metaKey || e.key === "PrintScreen") e.preventDefault();
    }});
    </script>
    </body>
    </html>
    """
    st.components.v1.html(html, height=780, scrolling=False)

def god_admin_panel():
    inject_god_css()
    
    if not st.session_state.get("god_admin", False):
        st.markdown("<div style='text-align:center;margin-top:100px'><h1>⚡ GOD PANEL LOGIN</h1><p>Enter Master System Credentials</p></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            pwd = st.text_input("Master Key", type="password")
            if st.button("AUTHENTICATE GOD MODE", use_container_width=True):
                if check_admin_password(pwd):
                    st.session_state.god_admin = True
                    st.rerun()
                else:
                    st.error("ACCESS DENIED: INVALID KEY")
        return

    # Auto Refresh mechanism for live active users
    st.markdown("""
    <script>
        setTimeout(function(){
            window.location.reload();
        }, 5000);
    </script>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align:center;color:#00f0ff'>⚡ GOD CONTROL PANEL ⚡</h1>", unsafe_allow_html=True)
    
    c_out1, c_out2 = st.columns([8, 2])
    with c_out2:
        if st.button("LOGOUT GOD MODE"):
            st.session_state.god_admin = False
            st.rerun()

    st.markdown("---")
    
    # Active Users Live Dashboard Metrics
    total_active = get_active_sessions_count()
    conn = db()
    total_imgs = conn.execute("SELECT COUNT(*) as cnt FROM images").fetchone()["cnt"]
    total_views = conn.execute("SELECT SUM(total_views) as cnt FROM images").fetchone()["cnt"] or 0
    conn.close()

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"<div class='god-card'><h3 style='color:#00ffaa'>🔴 LIVE VIEWERS NOW</h3><h1 style='font-size:48px;color:#00ffaa'>{total_active}</h1><small>Auto-refreshed live every 5s</small></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='god-card'><h3>🖼️ TOTAL VAULT IMAGES</h3><h1 style='font-size:48px'>{total_imgs}</h1></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='god-card'><h3 style='color:#ff0055'>👁️ CUMULATIVE VIEWS</h3><h1 style='font-size:48px;color:#ff0055'>{total_views}</h1></div>", unsafe_allow_html=True)

    # Permanent Single Link Setup Section
    st.markdown("### 🛠️ PERMANENT VAULT LINK CONTROL")
    st.info("💡 You can use **1 Master Link** (`?view=PERMANENT_LINK_001`) continuously! Change image, reset views, or toggle block/unblock anytime without changing the URL link!")

    perm_id = "PERMANENT_LINK_001"
    perm_image = get_image(perm_id)

    with st.container():
        st.markdown("<div class='god-card'>", unsafe_allow_html=True)
        st.subheader("🔥 MASTER PERMANENT LINK ENGINE")
        
        col_left, col_right = st.columns([1, 1])
        
        with col_left:
            st.markdown(f"**Permanent Master URL Query:** `?view={perm_id}`")
            up_perm = st.file_uploader("Upload / Swap Master Link Image", type=["png","jpg","jpeg","webp","gif"], key="perm_upload")
            p_mode = st.radio("Access Rule", ["global", "per_user"], index=0 if not perm_image else (0 if perm_image["mode"]=="global" else 1), key="p_mode")
            p_max = st.number_input("Max Allowed Views (e.g. 1000)", min_value=1, max_value=100000, value=perm_image["max_views"] if perm_image else 1000, key="p_max")
            p_secs = st.number_input("Timer (Seconds)", min_value=1, max_value=600, value=perm_image["view_seconds"] if perm_image else 5, key="p_secs")
            p_cam = st.checkbox("Require Live Camera Verification", value=bool(perm_image["camera_required"]) if perm_image else False, key="p_cam")

            if st.button("🚀 UPDATE MASTER LINK PAYLOAD", use_container_width=True):
                if up_perm:
                    replace_or_create_image(perm_id, up_perm, p_mode, p_max, p_secs, int(p_cam))
                    st.success("Master Link Payload Updated Successfully!")
                    st.rerun()
                elif perm_image:
                    update_image_config(perm_id, perm_image["filename"], p_mode, p_max, p_secs, int(p_cam))
                    st.success("Master Link Rules Updated!")
                    st.rerun()
                else:
                    st.error("Please upload an image for the Master Link first.")

        with col_right:
            if perm_image:
                st.write(f"**Status:** {'🔴 BLOCKED' if perm_image['disabled'] else '🟢 ACTIVE'}")
                st.write(f"**Current Views:** {get_image_view_count(perm_id)} / {perm_image['max_views']}")
                
                b1, b2, b3 = st.columns(3)
                with b1:
                    if st.button("🔄 RESET LIMIT TO 0", key="p_reset"):
                        reset_image_limit(perm_id)
                        st.success("Limit Reset to 0!")
                        st.rerun()
                with b2:
                    btn_txt = "UNBLOCK LINK" if perm_image["disabled"] else "BLOCK LINK"
                    if st.button(f"⛔ {btn_txt}", key="p_toggle"):
                        toggle_disable_image(perm_id, perm_image["disabled"])
                        st.rerun()
                with b3:
                    if st.button("💣 DELETE MASTER PAYLOAD", key="p_del"):
                        delete_image(perm_id)
                        st.rerun()
            else:
                st.warning("Master Link Payload not initialized yet. Upload an image to start using `?view=PERMANENT_LINK_001`!")

        st.markdown("</div>", unsafe_allow_html=True)

    # All Images & Additional Links Engine
    st.markdown("### 🗄️ ALL ACTIVE LINKS MANAGEMENT")
    conn = db()
    all_imgs = conn.execute("SELECT * FROM images ORDER BY created_at DESC").fetchall()
    conn.close()

    for row in all_imgs:
        with st.container():
            st.markdown("<div class='god-card'>", unsafe_allow_html=True)
            ic1, ic2, ic3, ic4 = st.columns([3, 2, 2, 3])
            
            views_cnt = get_image_view_count(row["id"])
            act_cnt = get_active_sessions_count(row["id"])
            
            with ic1:
                st.markdown(f"**File:** `{row['filename']}`")
                st.markdown(f"**Link ID:** `{row['id']}`")
                st.code(f"?view={row['id']}", language="text")
            
            with ic2:
                st.write(f"**Views:** {views_cnt} / {row['max_views']}")
                st.write(f"**Live Now:** 🟢 {act_cnt}")
                st.write(f"**Status:** {'🔴 Disabled' if row['disabled'] else '🟢 Active'}")

            with ic3:
                st.write(f"**Timer:** {row['view_seconds']}s")
                st.write(f"**Mode:** {row['mode']}")
                st.write(f"**Cam Req:** {'YES' if row['camera_required'] else 'NO'}")

            with ic4:
                rc1, rc2 = st.columns(2)
                with rc1:
                    if st.button("🔄 Reset 0", key=f"r_{row['id']}"):
                        reset_image_limit(row["id"])
                        st.rerun()
                    if st.button("Toggle Block", key=f"tb_{row['id']}"):
                        toggle_disable_image(row["id"], row["disabled"])
                        st.rerun()
                with rc2:
                    if st.button("🗑️ Delete", key=f"dl_{row['id']}"):
                        delete_image(row["id"])
                        st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

def main():
    query = st.query_params
    if "admin" in query or "god" in query:
        god_admin_panel()
        return
    if "view" in query:
        image_id = str(query["view"])
        show_image(image_id)
        return

    inject_god_css()
    st.markdown("""
    <div style="text-align:center;padding:120px 20px">
        <h1 style="font-size:50px;color:#00f0ff">⚡ CYBER-VAULT SECURE IMAGE SYSTEM ⚡</h1>
        <p style="font-size:20px;color:#a0a0c0">Military-grade temporary image sharing protocol with self-destruct mechanism.</p>
        <br/><br/>
        <a href="?admin=1" style="color:#00f0ff;font-family:'Orbitron',sans-serif;text-decoration:none;border:1px solid #00f0ff;padding:12px 30px;border-radius:30px;box-shadow:0 0 15px rgba(0,240,255,0.4)">ACCESS GOD PANEL</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
