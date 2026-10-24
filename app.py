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

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
UPLOAD_DIR = DATA_DIR / "images"
DB_PATH = DATA_DIR / "app.db"
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)

MIN_DISPLAY_SECONDS = 1
MAX_DISPLAY_SECONDS = 60
DEFAULT_DISPLAY_SECONDS = 3

st.set_page_config(page_title="Secure One-Time Image", page_icon="🔒", layout="centered")


def db():
    conn = sqlite3.connect(str(DB_PATH), timeout=30, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_column(conn, table_name, column_name, column_sql):
    columns = {row[1].lower() for row in conn.execute(f"PRAGMA table_info({table_name})").fetchall()}
    if column_name.lower() in columns:
        return
    try:
        conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_sql}")
    except sqlite3.OperationalError as exc:
        if "duplicate column name" not in str(exc).lower():
            raise


def migrate_db():
    conn = db()
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute(
            """CREATE TABLE IF NOT EXISTS images (
                id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                stored_filename TEXT NOT NULL,
                mode TEXT NOT NULL,
                display_seconds INTEGER NOT NULL DEFAULT 3,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                disabled INTEGER NOT NULL DEFAULT 0,
                total_views INTEGER NOT NULL DEFAULT 0
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS locks (
                image_id TEXT NOT NULL,
                viewer_id TEXT NOT NULL,
                locked_at TEXT NOT NULL,
                ip_hash TEXT,
                user_agent_hash TEXT,
                PRIMARY KEY (image_id, viewer_id)
            )"""
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_images_created_at ON images(created_at)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_images_mode ON images(mode)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_locks_image_id ON locks(image_id)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_locks_viewer_id ON locks(viewer_id)")

        ensure_column(conn, "images", "display_seconds", "display_seconds INTEGER NOT NULL DEFAULT 3")
        ensure_column(conn, "images", "updated_at", "updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP")
        ensure_column(conn, "images", "disabled", "disabled INTEGER NOT NULL DEFAULT 0")
        ensure_column(conn, "images", "total_views", "total_views INTEGER NOT NULL DEFAULT 0")

        ensure_column(conn, "locks", "ip_hash", "ip_hash TEXT")
        ensure_column(conn, "locks", "user_agent_hash", "user_agent_hash TEXT")

        conn.execute(
            "UPDATE images SET display_seconds = 3 WHERE display_seconds IS NULL OR display_seconds < 1"
        )
        conn.execute(
            "UPDATE images SET disabled = 0 WHERE disabled IS NULL"
        )
        conn.execute(
            "UPDATE images SET total_views = 0 WHERE total_views IS NULL"
        )
        conn.execute(
            "UPDATE images SET updated_at = created_at WHERE updated_at IS NULL OR updated_at = ''"
        )

        conn.commit()
    finally:
        conn.close()


migrate_db()


def get_secret(name, default=""):
    try:
        value = st.secrets.get(name)
        if value not in (None, ""):
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


def clamp_display_seconds(value):
    try:
        seconds = int(value)
    except (TypeError, ValueError):
        return DEFAULT_DISPLAY_SECONDS
    if seconds < MIN_DISPLAY_SECONDS:
        return MIN_DISPLAY_SECONDS
    if seconds > MAX_DISPLAY_SECONDS:
        return MAX_DISPLAY_SECONDS
    return seconds


def get_image(image_id):
    conn = db()
    row = conn.execute("SELECT * FROM images WHERE id=?", (image_id,)).fetchone()
    conn.close()
    return row


def already_locked(image_id, viewer_id):
    conn = db()
    row = conn.execute(
        "SELECT 1 FROM locks WHERE image_id=? AND viewer_id=? LIMIT 1",
        (image_id, viewer_id),
    ).fetchone()
    conn.close()
    return row is not None


def global_already_viewed(image_id):
    conn = db()
    row = conn.execute(
        "SELECT 1 FROM locks WHERE image_id=? LIMIT 1",
        (image_id,),
    ).fetchone()
    conn.close()
    return row is not None


def reset_image(image_id):
    now = datetime.now(timezone.utc).isoformat()
    conn = db()
    try:
        conn.execute("DELETE FROM locks WHERE image_id=?", (image_id,))
        conn.execute(
            "UPDATE images SET total_views=0, updated_at=? WHERE id=?",
            (now, image_id),
        )
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()


def disable_image(image_id):
    conn = db()
    conn.execute(
        "UPDATE images SET disabled=1, updated_at=? WHERE id=?",
        (datetime.now(timezone.utc).isoformat(), image_id),
    )
    conn.commit()
    conn.close()


def enable_image(image_id):
    conn = db()
    conn.execute(
        "UPDATE images SET disabled=0, updated_at=? WHERE id=?",
        (datetime.now(timezone.utc).isoformat(), image_id),
    )
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
    try:
        conn.execute("DELETE FROM locks WHERE image_id=?", (image_id,))
        conn.execute("DELETE FROM images WHERE id=?", (image_id,))
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()


def image_to_data_uri(path):
    mime = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(path.suffix.lower())
    if not mime:
        raise ValueError("Unsupported image format")
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:{mime};base64,{encoded}"


def create_image(uploaded_file, mode, display_seconds=DEFAULT_DISPLAY_SECONDS):
    image_id = uuid.uuid4().hex
    extension = Path(uploaded_file.name).suffix.lower()
    if extension not in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
        raise ValueError("Only PNG, JPG, JPEG, WEBP and GIF are allowed.")

    data = uploaded_file.getvalue()
    if len(data) > 20 * 1024 * 1024:
        raise ValueError("Image is larger than 20 MB.")

    try:
        Image.open(io.BytesIO(data)).verify()
    except Exception as exc:
        raise ValueError("Uploaded file is not a valid image.") from exc

    stored_filename = image_id + extension
    with open(UPLOAD_DIR / stored_filename, "wb") as f:
        f.write(data)

    now = datetime.now(timezone.utc).isoformat()
    conn = db()
    try:
        conn.execute(
            """INSERT INTO images (
                id, filename, stored_filename, mode, display_seconds, created_at, updated_at, disabled, total_views
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0)""",
            (
                image_id,
                uploaded_file.name,
                stored_filename,
                mode,
                clamp_display_seconds(display_seconds),
                now,
                now,
            ),
        )
        conn.commit()
        return image_id
    finally:
        conn.close()


def check_admin_password(password):
    configured = get_secret("ADMIN_PASSWORD")
    if not configured:
        return False
    return bool(configured) and hmac.compare_digest(password, configured)


def set_image_display_seconds(image_id, seconds):
    value = clamp_display_seconds(seconds)
    conn = db()
    try:
        conn.execute(
            "UPDATE images SET display_seconds=?, updated_at=? WHERE id=?",
            (value, datetime.now(timezone.utc).isoformat(), image_id),
        )
        conn.commit()
        return True
    except Exception:
        conn.rollback()
        return False
    finally:
        conn.close()


def acquire_view_lock(image_id, viewer_id):
    conn = db()
    try:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute("SELECT * FROM images WHERE id=?", (image_id,)).fetchone()
        if row is None:
            conn.rollback()
            return False, "missing"
        if bool(row["disabled"]):
            conn.rollback()
            return False, "disabled"

        if row["mode"] == "global":
            existing = conn.execute(
                "SELECT 1 FROM locks WHERE image_id=? LIMIT 1",
                (image_id,),
            ).fetchone()
            if existing is not None:
                conn.rollback()
                return False, "already_viewed"
        elif row["mode"] == "per_user":
            existing = conn.execute(
                "SELECT 1 FROM locks WHERE image_id=? AND viewer_id=? LIMIT 1",
                (image_id, viewer_id),
            ).fetchone()
            if existing is not None:
                conn.rollback()
                return False, "already_viewed_for_user"

        now = datetime.now(timezone.utc).isoformat()
        conn.execute(
            """INSERT INTO locks (image_id, viewer_id, locked_at, ip_hash, user_agent_hash)
            VALUES (?, ?, ?, ?, ?)""",
            (
                image_id,
                viewer_id,
                now,
                hmac_hash(get_client_ip()),
                hmac_hash(get_user_agent()),
            ),
        )
        conn.execute(
            "UPDATE images SET total_views=total_views+1, updated_at=? WHERE id=?",
            (now, image_id),
        )
        conn.commit()
        return True, row
    except Exception:
        conn.rollback()
        return False, "error"
    finally:
        conn.close()


def get_stats():
    conn = db()
    stats = conn.execute(
        """
        SELECT
            COUNT(*) AS total_images,
            SUM(CASE WHEN disabled = 0 THEN 1 ELSE 0 END) AS enabled_images,
            SUM(CASE WHEN disabled = 1 THEN 1 ELSE 0 END) AS disabled_images,
            COALESCE(SUM(total_views), 0) AS total_views,
            COALESCE((SELECT COUNT(*) FROM locks), 0) AS active_locks
        FROM images
        """
    ).fetchone()
    conn.close()
    return stats


def list_images():
    conn = db()
    rows = conn.execute(
        "SELECT * FROM images ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return rows


def render_image_html(data_uri, display_seconds):
    return f"""<!DOCTYPE html><html><head>
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
    <h2>Image no longer available</h2></div></div>
    <script>
    const image=document.getElementById("secureImage");
    const expired=document.getElementById("expired");
    setTimeout(() => {{image.remove();expired.style.display="block";}}, {display_seconds * 1000});
    document.addEventListener("contextmenu", e => e.preventDefault());
    document.addEventListener("dragstart", e => e.preventDefault());
    document.addEventListener("selectstart", e => e.preventDefault());
    document.addEventListener("keydown", e => {{
      if (e.ctrlKey && ["s","S","u","U","c","C"].includes(e.key)) e.preventDefault();
      if (e.key === "PrintScreen") e.preventDefault();
    }});
    </script></body></html>"""


def show_locked_message():
    st.markdown(
        """<div style="text-align:center;padding:60px 20px">
        <h1>🔒</h1><h2>Image no longer available</h2>
        <p>This image has already been viewed, is disabled, or is not available.</p></div>""",
        unsafe_allow_html=True,
    )


def show_image(image_id):
    row = get_image(image_id)
    if not row or bool(row["disabled"]):
        show_locked_message()
        return

    viewer_id = make_viewer_id()
    allowed, reason = acquire_view_lock(image_id, viewer_id)
    if not allowed:
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

    display_seconds = clamp_display_seconds(row["display_seconds"])
    st.components.v1.html(render_image_html(data_uri, display_seconds), height=700, scrolling=False)


def admin_panel():
    if not st.session_state.get("admin", False):
        st.markdown("<h2 style='text-align:center'>🔐 Admin Login</h2>", unsafe_allow_html=True)
        password = st.text_input("Admin password", type="password")
        if st.button("Login", use_container_width=True):
            if check_admin_password(password):
                st.session_state.admin = True
                st.rerun()
            else:
                st.error("Invalid password.")
        return

    st.title("🔐 Secure Image Admin")
    if st.button("Logout"):
        st.session_state.admin = False
        st.rerun()

    st.divider()

    stats = get_stats()
    st.subheader("Statistics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Images", stats["total_images"] or 0)
    c2.metric("Enabled", stats["enabled_images"] or 0)
    c3.metric("Disabled", stats["disabled_images"] or 0)
    c4.metric("Total views", stats["total_views"] or 0)
    st.caption(f"Active locks: {stats['active_locks'] or 0}")

    st.divider()
    st.subheader("Create one-time image")
    uploaded = st.file_uploader("Choose image", type=["png", "jpg", "jpeg", "webp", "gif"])
    mode = st.radio(
        "Lock mode",
        ["per_user", "global"],
        format_func=lambda x: "Per-user one-time lock" if x == "per_user" else "Global one-time lock",
    )
    display_seconds = st.slider(
        "Display duration (seconds)",
        min_value=MIN_DISPLAY_SECONDS,
        max_value=MAX_DISPLAY_SECONDS,
        value=DEFAULT_DISPLAY_SECONDS,
        step=1,
    )

    if uploaded:
        st.image(uploaded, caption="Preview")
        if st.button("🔒 Create Secure Link", type="primary", use_container_width=True):
            try:
                image_id = create_image(uploaded, mode, display_seconds)
                st.success("Secure image created.")
                st.code(f"?view={image_id}", language="text")
                st.info("Append this query to your deployed Streamlit URL to share the image.")
            except Exception as exc:
                st.error(f"Could not create image: {exc}")

    st.divider()
    st.subheader("Image management")
    rows = list_images()
    if not rows:
        st.info("No images created yet.")
        return

    for row in rows:
        with st.container(border=True):
            st.write(f"**{row['filename']}**")
            st.write(f"ID: `{row['id']}`")
            st.write(f"Link: `?view={row['id']}`")
            st.write(f"Mode: `{row['mode']}`")
            st.write(f"Views: `{row['total_views']}`")
            st.write(f"Display: `{row['display_seconds']}s`")
            st.write(f"Disabled: `{bool(row['disabled'])}`")

            with st.form(f"edit_{row['id']}"):
                new_duration = st.slider(
                    "Display duration",
                    min_value=MIN_DISPLAY_SECONDS,
                    max_value=MAX_DISPLAY_SECONDS,
                    value=clamp_display_seconds(row["display_seconds"]),
                    key=f"timer_{row['id']}",
                    label_visibility="collapsed",
                )
                submitted = st.form_submit_button("Save duration")
                if submitted:
                    set_image_display_seconds(row["id"], new_duration)
                    st.rerun()

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button(
                    "Reset link",
                    key=f"reset_{row['id']}",
                    use_container_width=True,
                ):
                    reset_image(row["id"])
                    st.rerun()
            with c2:
                action_label = "Enable" if row["disabled"] else "Disable"
                if st.button(
                    action_label,
                    key=f"toggle_{row['id']}",
                    use_container_width=True,
                ):
                    if row["disabled"]:
                        enable_image(row["id"])
                    else:
                        disable_image(row["id"])
                    st.rerun()
            with c3:
                if st.button(
                    "Delete permanently",
                    key=f"delete_{row['id']}",
                    use_container_width=True,
                ):
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

    st.markdown(
        """<div style="text-align:center;padding-top:80px">
        <h1>🔒 Secure Image</h1><p>One-time temporary image viewer.</p></div>""",
        unsafe_allow_html=True,
    )
    st.info("This page does not contain an image.")
    st.write("Use the admin URL to create a secure image and generate a permanent link.")
    st.code("?admin=1", language="text")


if __name__ == "__main__":
    main()
