from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests
import streamlit as st


st.set_page_config(page_title="OpenRoom Chat", page_icon="O", layout="wide")

ROOMS = {"general": "General", "study": "Study room", "lounge": "Lounge"}
MAX_MESSAGE_LENGTH = 1000
AUTH_BASE = "https://identitytoolkit.googleapis.com/v1"
TOKEN_BASE = "https://securetoken.googleapis.com/v1"


class FirebaseError(Exception):
    pass


def get_setting(name: str, default: str = "") -> str:
    try:
        value = st.secrets[name]
        if value is not None:
            return str(value)
    except Exception:
        pass
    return os.getenv(name, default)


def get_config() -> dict[str, Any]:
    admin_emails = {
        value.strip().lower()
        for value in get_setting("ADMIN_EMAILS").split(",")
        if value.strip()
    }
    return {
        "api_key": get_setting("FIREBASE_API_KEY"),
        "database_url": get_setting("FIREBASE_DATABASE_URL").rstrip("/"),
        "admin_emails": admin_emails,
    }


def firebase_error(response: requests.Response) -> FirebaseError:
    try:
        message = response.json().get("error", {}).get("message", "Firebase request failed")
    except (ValueError, AttributeError):
        message = "Firebase request failed"
    friendly = {
        "EMAIL_EXISTS": "An account already exists for that email.",
        "INVALID_EMAIL": "Enter a valid email address.",
        "WEAK_PASSWORD": "Choose a password with at least 6 characters.",
        "EMAIL_NOT_FOUND": "No account was found for that email.",
        "INVALID_PASSWORD": "The password is incorrect.",
        "INVALID_LOGIN_CREDENTIALS": "The email or password is incorrect.",
        "USER_DISABLED": "This account has been disabled.",
        "TOO_MANY_ATTEMPTS_TRY_LATER": "Too many attempts. Try again later.",
        "API_KEY_INVALID": "The Firebase API key is invalid.",
        "TOKEN_EXPIRED": "Your session expired. Please sign in again.",
        "PERMISSION_DENIED": "Firebase denied this action. Check the database rules setup.",
    }
    return FirebaseError(friendly.get(message, message.replace("_", " ").capitalize()))


def auth_request(action: str, api_key: str, payload: dict[str, Any]) -> dict[str, Any]:
    try:
        response = requests.post(
            f"{AUTH_BASE}/accounts:{action}",
            params={"key": api_key},
            json=payload,
            timeout=12,
        )
    except requests.RequestException as exc:
        raise FirebaseError("Could not reach Firebase Authentication.") from exc
    if not response.ok:
        raise firebase_error(response)
    return response.json()


def send_verification_email(api_key: str, id_token: str) -> None:
    try:
        response = requests.post(
            f"{AUTH_BASE}/accounts:sendOobCode",
            params={"key": api_key},
            json={"requestType": "VERIFY_EMAIL", "idToken": id_token},
            timeout=12,
        )
    except requests.RequestException as exc:
        raise FirebaseError("Could not reach Firebase Authentication.") from exc
    if not response.ok:
        raise firebase_error(response)


def refresh_session(config: dict[str, Any]) -> bool:
    user = st.session_state.get("chat_user")
    if not user:
        return False
    if time.time() < user["expires_at"] - 90:
        return True
    try:
        response = requests.post(
            f"{TOKEN_BASE}/token",
            params={"key": config["api_key"]},
            data={"grant_type": "refresh_token", "refresh_token": user["refresh_token"]},
            timeout=12,
        )
        if not response.ok:
            raise firebase_error(response)
        token_data = response.json()
        user["id_token"] = token_data["id_token"]
        user["refresh_token"] = token_data.get("refresh_token", user["refresh_token"])
        user["expires_at"] = time.time() + int(token_data.get("expires_in", 3600))
        return True
    except (requests.RequestException, FirebaseError, KeyError, ValueError):
        st.session_state.pop("chat_user", None)
        st.session_state.pop("chat_unverified_user", None)
        return False


def database_request(
    method: str,
    path: str,
    config: dict[str, Any],
    user: dict[str, Any],
    *,
    payload: Any = None,
    params: dict[str, Any] | None = None,
) -> Any:
    encoded_path = quote(path.strip("/"), safe="/")
    query = dict(params or {})
    query["auth"] = user["id_token"]
    try:
        response = requests.request(
            method,
            f"{config['database_url']}/{encoded_path}.json",
            params=query,
            json=payload,
            timeout=12,
        )
    except requests.RequestException as exc:
        raise FirebaseError("Could not reach the Firebase Realtime Database.") from exc
    if not response.ok:
        raise firebase_error(response)
    if response.status_code == 204 or not response.content:
        return None
    return response.json()


def load_messages(
    config: dict[str, Any], user: dict[str, Any], room_id: str
) -> list[dict[str, Any]]:
    data = database_request(
        "GET",
        f"rooms/{room_id}/messages",
        config,
        user,
        params={"orderBy": '"createdAt"', "limitToLast": "100"},
    )
    messages = []
    for key, message in (data or {}).items():
        if isinstance(message, dict):
            messages.append({**message, "key": key})
    return sorted(messages, key=lambda message: message.get("createdAt", 0))


def load_all_messages(config: dict[str, Any], user: dict[str, Any]) -> list[dict[str, Any]]:
    messages = []
    for room_id, room_name in ROOMS.items():
        for message in load_messages(config, user, room_id):
            messages.append({**message, "roomId": room_id, "roomName": room_name})
    return sorted(messages, key=lambda message: message.get("createdAt", 0), reverse=True)


def apply_styles() -> None:
    css_path = Path(__file__).with_name("styles.css")
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def show_setup() -> None:
    st.title("OpenRoom")
    st.write("A real-time chat app with Firebase sign-in, rooms, and a moderator console.")
    st.warning("Connect a Firebase project to enable chat.")
    st.markdown(
        """
        1. Create a Firebase project and enable **Authentication → Email/Password**.
        2. Create a **Realtime Database** and copy its database URL.
        3. Add the configuration below to `.streamlit/secrets.toml` (or environment variables).
        4. Apply the rules from `firebase.rules.json`, replacing the example moderator email.

        ```toml
        FIREBASE_API_KEY = "your-web-api-key"
        FIREBASE_DATABASE_URL = "https://your-project-default-rtdb.region.firebasedatabase.app"
        ADMIN_EMAILS = "moderator@example.com"
        ```

        `ADMIN_EMAILS` accepts a comma-separated list. Do not put a Firebase service-account key in this app.
        """
    )


def store_session(auth_data: dict[str, Any]) -> dict[str, Any]:
    return {
        "uid": auth_data["localId"],
        "email": auth_data["email"].lower(),
        "email_verified": bool(auth_data.get("emailVerified", False)),
        "id_token": auth_data["idToken"],
        "refresh_token": auth_data["refreshToken"],
        "expires_at": time.time() + int(auth_data.get("expiresIn", 3600)),
    }


def auth_screen(config: dict[str, Any]) -> None:
    st.title("OpenRoom")
    st.caption("A quieter place to talk, learn, and share ideas.")
    sign_in_tab, create_tab = st.tabs(["Sign in", "Create account"])

    with sign_in_tab:
        with st.form("signin_form"):
            email = st.text_input("Email", key="signin_email", autocomplete="email")
            password = st.text_input("Password", type="password", key="signin_password", autocomplete="current-password")
            submitted = st.form_submit_button("Sign in", use_container_width=True)
        if submitted:
            try:
                result = auth_request(
                    "signInWithPassword",
                    config["api_key"],
                    {"email": email.strip(), "password": password, "returnSecureToken": True},
                )
                user = store_session(result)
                if user["email_verified"]:
                    st.session_state.chat_user = user
                    st.rerun()
                else:
                    st.session_state.chat_unverified_user = user
                    st.warning("Verify your email before entering the chat.")
            except FirebaseError as exc:
                st.error(str(exc))

        unverified = st.session_state.get("chat_unverified_user")
        if unverified:
            st.info(f"Verification is required for {unverified['email']}.")
            left, right = st.columns(2)
            if left.button("Resend verification email", use_container_width=True):
                try:
                    send_verification_email(config["api_key"], unverified["id_token"])
                    st.success("Verification email sent. Check your inbox, then sign in again.")
                except FirebaseError as exc:
                    st.error(str(exc))
            if right.button("Clear pending account", use_container_width=True):
                st.session_state.pop("chat_unverified_user", None)
                st.rerun()

        with st.form("reset_form"):
            reset_email = st.text_input("Email for password reset", key="reset_email")
            reset = st.form_submit_button("Send password reset")
        if reset:
            try:
                response = requests.post(
                    f"{AUTH_BASE}/accounts:sendOobCode",
                    params={"key": config["api_key"]},
                    json={"requestType": "PASSWORD_RESET", "email": reset_email.strip()},
                    timeout=12,
                )
                if not response.ok:
                    raise firebase_error(response)
                st.success("If that account exists, Firebase has sent a password reset email.")
            except (requests.RequestException, FirebaseError) as exc:
                st.error(str(exc))

    with create_tab:
        with st.form("signup_form"):
            email = st.text_input("Email address", key="signup_email", autocomplete="email")
            password = st.text_input("Password", type="password", key="signup_password", autocomplete="new-password")
            confirm = st.text_input("Confirm password", type="password", key="signup_confirm")
            submitted = st.form_submit_button("Create account", use_container_width=True)
        if submitted:
            if password != confirm:
                st.error("The passwords do not match.")
            elif len(password) < 6:
                st.error("Use a password with at least 6 characters.")
            else:
                try:
                    result = auth_request(
                        "signUp",
                        config["api_key"],
                        {"email": email.strip(), "password": password, "returnSecureToken": True},
                    )
                    user = store_session(result)
                    send_verification_email(config["api_key"], user["id_token"])
                    st.session_state.chat_unverified_user = user
                    st.success("Account created. Verify your email before signing in.")
                except FirebaseError as exc:
                    st.error(str(exc))


def render_chat(config: dict[str, Any], user: dict[str, Any], room_id: str) -> None:
    room_name = ROOMS[room_id]

    @st.fragment(run_every="3s")
    def live_messages() -> None:
        if not refresh_session(config):
            st.rerun()
        try:
            messages = load_messages(config, user, room_id)
        except FirebaseError as exc:
            st.error(str(exc))
            return

        if not messages:
            st.markdown('<div class="empty-room">No messages yet. Start the conversation.</div>', unsafe_allow_html=True)
        for message in messages:
            is_self = message.get("uid") == user["uid"]
            with st.chat_message("user" if is_self else "assistant"):
                st.caption("You" if is_self else message.get("email", "Member"))
                st.text(message.get("text", ""))

        text = st.chat_input(f"Message {room_name}…", max_chars=MAX_MESSAGE_LENGTH, key=f"chat_input_{room_id}")
        if text and text.strip():
            try:
                database_request(
                    "POST",
                    f"rooms/{room_id}/messages",
                    config,
                    user,
                    payload={
                        "uid": user["uid"],
                        "email": user["email"],
                        "text": text.strip(),
                        "createdAt": int(time.time() * 1000),
                    },
                )
                st.rerun(scope="fragment")
            except FirebaseError as exc:
                st.error(str(exc))

    live_messages()


def moderation_panel(config: dict[str, Any], user: dict[str, Any]) -> None:
    st.subheader("Moderation")
    st.caption("Recent messages across rooms. Deleting a message permanently removes it from Firebase.")
    if st.button("Refresh moderation queue", icon=":material/refresh:"):
        st.rerun()
    try:
        messages = load_all_messages(config, user)
    except FirebaseError as exc:
        st.error(str(exc))
        return
    if not messages:
        st.info("There are no messages to review.")
        return

    for message in messages:
        with st.container(border=True):
            meta, action = st.columns([5, 1])
            timestamp = message.get("createdAt", 0)
            created = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime(timestamp / 1000)) if timestamp else "Time unavailable"
            meta.caption(f"#{message['roomName']} · {message.get('email', 'Member')} · {created}")
            meta.text(message.get("text", ""))
            if action.button("Delete", key=f"delete_{message['roomId']}_{message['key']}", type="secondary"):
                try:
                    database_request(
                        "DELETE",
                        f"rooms/{message['roomId']}/messages/{message['key']}",
                        config,
                        user,
                    )
                    st.toast("Message deleted")
                    st.rerun()
                except FirebaseError as exc:
                    st.error(str(exc))


def main() -> None:
    apply_styles()
    config = get_config()
    if not config["api_key"] or not config["database_url"]:
        show_setup()
        return

    user = st.session_state.get("chat_user")
    if user and not refresh_session(config):
        user = None
    if not user:
        auth_screen(config)
        return

    is_admin = user["email"] in config["admin_emails"]
    with st.sidebar:
        st.markdown("# OpenRoom")
        st.caption("REAL PEOPLE · GOOD CONVERSATIONS")
        room_id = st.selectbox(
            "Room",
            list(ROOMS),
            format_func=lambda value: ROOMS[value],
            key="selected_room",
        )
        page = "Chat"
        if is_admin:
            page = st.radio("Workspace", ["Chat", "Moderation"], horizontal=True)
        st.divider()
        st.caption(f"Signed in as **{user['email']}**")
        if is_admin:
            st.caption("Moderator access")
        if st.button("Sign out", use_container_width=True):
            st.session_state.pop("chat_user", None)
            st.rerun()

    st.title(f"{ROOMS[room_id] if page == 'Chat' else 'Moderator console'}")
    st.caption("Messages refresh automatically. Be kind, and don't share sensitive personal information.")
    if page == "Moderation":
        moderation_panel(config, user)
    else:
        render_chat(config, user, room_id)


if __name__ == "__main__":
    main()