import os
import io
import uuid
import hmac
import hashlib
import sqlite3
import base64
from pathlib import Path
from datetime import datetime, timezone

import streamlit as st
from PIL import Image

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
UPLOAD_DIR = DATA_DIR / "images"
DB_PATH = DATA_DIR / "app.db"
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="Secure One-Time Image", page_icon="🔒", layout="centered")

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
        mode TEXT NOT NULL, 
        created_at TEXT NOT NULL, 
        disabled INTEGER DEFAULT 0,
        total_views INTEGER DEFAULT 0,
        max_views INTEGER DEFAULT 1,
        view_duration INTEGER DEFAULT 3)""")
    
    # Safe column additions for legacy DB schemas
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(images)")
    columns = [row[1] for row in cursor.fetchall()]
    if "max_views" not in columns:
        conn.execute("ALTER TABLE images ADD COLUMN max_views INTEGER DEFAULT 1")
    if "view_duration" not in columns:
        conn.execute("ALTER TABLE images ADD COLUMN view_duration INTEGER DEFAULT 3")

    conn.execute("""CREATE TABLE IF NOT EXISTS locks (
        image_id TEXT NOT NULL, 
        viewer_id TEXT NOT NULL, 
        locked_at TEXT NOT NULL,
        ip_hash TEXT, 
        user_agent_hash TEXT)""")
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
    return get_secret("APP_SECRET", "CHANGE_THIS_SECRET")

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
    return "unknown"

def get_user_agent():
    try:
        return st.context.headers.get("User-Agent", "unknown")
    except Exception:
        return "unknown"

def make_viewer_id():
    return hmac_hash(f"{get_client_ip()}|{get_user_agent()}")

def get_image(image_id):
    conn = db()
    row = conn.execute("SELECT * FROM images WHERE id=?", (image_id,)).fetchone()
    conn.close()
    return row

def get_viewer_lock_count(image_id, viewer_id):
    conn = db()
    row = conn.execute(
        "SELECT COUNT(*) as count FROM locks WHERE image_id=? AND viewer_id=?",
        (image_id, viewer_id)).fetchone()
    conn.close()
    return row["count"] if row else 0

def get_global_lock_count(image_id):
    conn = db()
    row = conn.execute(
        "SELECT COUNT(*) as count FROM locks WHERE image_id=?",
        (image_id,)).fetchone()
    conn.close()
    return row["count"] if row else 0

def permanently_lock(image_id, viewer_id):
    now = datetime.now(timezone.utc).isoformat()
    conn = db()
    try:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute("""INSERT INTO locks
            (image_id, viewer_id, locked_at, ip_hash, user_agent_hash)
            VALUES (?, ?, ?, ?, ?)""",
            (image_id, viewer_id, now, hmac_hash(get_client_ip()), hmac_hash(get_user_agent())))
        conn.execute("UPDATE images SET total_views=total_views+1 WHERE id=?", (image_id,))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()

def disable_image(image_id):
    conn = db()
    conn.execute("UPDATE images SET disabled=1 WHERE id=?", (image_id,))
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
    conn.execute("DELETE FROM images WHERE id=?", (image_id,))
    conn.commit()
    conn.close()

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

def create_image(uploaded_file, mode, max_views=1, view_duration=3):
    image_id = uuid.uuid4().hex
    extension = Path(uploaded_file.name).suffix.lower()
    if extension not in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
        raise ValueError("Only PNG, JPG, JPEG, WEBP and GIF are allowed.")
    data = uploaded_file.getvalue()
    if len(data) > 20 * 1024 * 1024:
        raise ValueError("Image is larger than 20 MB.")
    try:
        Image.open(io.BytesIO(data)).verify()
    except Exception:
        raise ValueError("Uploaded file is not a valid image.")
    stored_filename = image_id + extension
    with open(UPLOAD_DIR / stored_filename, "wb") as f:
        f.write(data)
    conn = db()
    conn.execute("""INSERT INTO images
        (id, filename, stored_filename, mode, created_at, disabled, total_views, max_views, view_duration)
        VALUES (?, ?, ?, ?, ?, 0, 0, ?, ?)""",
        (image_id, uploaded_file.name, stored_filename, mode,
         datetime.now(timezone.utc).isoformat(), max_views, view_duration))
    conn.commit()
    conn.close()
    return image_id

def check_admin_password(password):
    configured = get_secret("ADMIN_PASSWORD")
    if not configured:
        # Default fallback password for first setup (Change this or set st.secrets["ADMIN_PASSWORD"])
        configured = "admin123" 
    return hmac.compare_digest(password, configured)

def show_locked_message():
    st.markdown("""<div style="text-align:center;padding:60px 20px">
    <h1>🔒</h1><h2>Image no longer available</h2>
    <p>This image view limit has been reached or it has been locked.</p></div>""", unsafe_allow_html=True)

def show_image(image_id):
    row = get_image(image_id)
    if not row or row["disabled"]:
        show_locked_message()
        return

    viewer_id = make_viewer_id()
    max_views = row["max_views"] if "max_views" in row.keys() and row["max_views"] else 1
    duration = row["view_duration"] if "view_duration" in row.keys() and row["view_duration"] else 3

    if row["mode"] == "global" and get_global_lock_count(image_id) >= max_views:
        show_locked_message()
        return
    if row["mode"] == "per_user" and get_viewer_lock_count(image_id, viewer_id) >= max_views:
        show_locked_message()
        return

    if not permanently_lock(image_id, viewer_id):
        show_locked_message()
        return

    file_path = UPLOAD_DIR / row["stored_filename"]
    if not file_path.exists():
        show_locked_message()
        return

    try:
        data_uri = image_to_data_uri(file_path)
    except Exception:
        show_locked_message()
        return

    html = f"""<!DOCTYPE html><html><head>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
    html,body{{margin:0;padding:0;width:100%;height:100%;background:#000;overflow:hidden;
    user-select:none;-webkit-user-select:none;-webkit-touch-callout:none}}
    #viewer{{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;
    background:#000;z-index:999999}}
    #secureImage{{max-width:100vw;max-height:100vh;object-fit:contain;pointer-events:none;
    user-select:none;-webkit-user-select:none;-webkit-touch-callout:none;-webkit-user-drag:none}}
    #expired{{display:none;color:#fff;text-align:center;font-family:Arial,sans-serif}}
    </style></head><body>
    <div id="viewer"><img id="secureImage" src="{data_uri}" draggable="false"
    oncontextmenu="return false"><div id="expired"><h1>🔒</h1>
    <h2>Image view time expired</h2></div></div>
    <script>
    const image=document.getElementById("secureImage");
    const expired=document.getElementById("expired");
    setTimeout(()=>{{image.remove();expired.style.display="block";}},{duration*1000});
    document.addEventListener("contextmenu",e=>e.preventDefault());
    document.addEventListener("dragstart",e=>e.preventDefault());
    document.addEventListener("selectstart",e=>e.preventDefault());
    document.addEventListener("keydown",e=>{{
      if(e.ctrlKey&&["s","S","u","U","c","C"].includes(e.key))e.preventDefault();
      if(e.key==="PrintScreen")e.preventDefault();
    }});
    </script></body></html>"""
    st.components.v1.html(html, height=700, scrolling=False)

def admin_panel():
    if not st.session_state.get("admin", False):
        st.markdown("<h2 style='text-align:center'>🔒 Admin Login</h2>", unsafe_allow_html=True)
        password = st.text_input("Admin password", type="password")
        if st.button("Login", use_container_width=True):
            if check_admin_password(password):
                st.session_state.admin = True
                st.rerun()
            else:
                st.error("Invalid password.")
        return

    st.title("🔑 Secure Image Admin Panel")
    if st.button("Logout"):
        st.session_state.admin = False
        st.rerun()

    st.divider()
    st.subheader("➕ Create New Secure Link")
    uploaded = st.file_uploader("Choose image", type=["png","jpg","jpeg","webp","gif"])
    
    col1, col2 = st.columns(2)
    with col1:
        max_views = st.number_input("Max Allowed Views (1-1000)", min_value=1, max_value=1000, value=1)
    with col2:
        view_duration = st.number_input("Display Time Limit (Seconds)", min_value=1, max_value=300, value=3)

    mode = st.radio("Lock mode", ["per_user","global"],
        format_func=lambda x: "Per-user view limit" if x=="per_user" else "Global view limit across all users")

    if uploaded:
        st.image(uploaded, caption="Preview", width=250)
        if st.button("🔒 Create Secure Link", type="primary", use_container_width=True):
            try:
                image_id = create_image(uploaded, mode, max_views, view_duration)
                st.success("Secure image created successfully!")
                link = f"?view={image_id}"
                st.code(link, language="text")
                st.info("Direct Link Parameter: " + link)
            except Exception as e:
                st.error(f"Could not create image: {e}")

    st.divider()
    st.subheader("📋 Active Images Management")
    conn = db()
    rows = conn.execute("SELECT * FROM images ORDER BY created_at DESC").fetchall()
    conn.close()

    if not rows:
        st.info("No images created yet.")
        return

    for row in rows:
        with st.container(border=True):
            st.write(f"**Filename:** `{row['filename']}`")
            st.write(f"**ID:** `{row['id']}`")
            st.write(f"**Mode:** `{row['mode']}` | **Max Views Allowed:** `{row['max_views']}`")
            st.write(f"**Total Views So Far:** `{row['total_views']}` | **Timer:** `{row['view_duration']}s`")
            st.write(f"**Status:** {'❌ Disabled' if row['disabled'] else '✅ Active'}")
            
            st.code(f"?view={row['id']}", language="text")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Disable Link", key=f"d_{row['id']}", use_container_width=True):
                    disable_image(row["id"])
                    st.rerun()
            with c2:
                if st.button("Delete Image", key=f"x_{row['id']}", use_container_width=True):
                    delete_image(row["id"])
                    st.rerun()

def main():
    query = st.query_params
    if "admin" in query:
        admin_panel()
        return
    if "view" in query:
        image_id = str(query["view"])
        if len(image_id) != 32 or not all(c in "0123456789abcdef" for c in image_id.lower()):
            show_locked_message()
            return
        show_image(image_id)
        return
    st.markdown("""<div style="text-align:center;padding-top:80px">
    <h1>🔒 Secure Image Viewer</h1><p>One-time/Limited temporary image viewer.</p></div>""",
    unsafe_allow_html=True)
    st.info("This page requires a valid secure link parameter.")
    st.write("Access the admin section to generate shareable links.")
    st.code("?admin=1", language="text")

if __name__ == "__main__":
    main()