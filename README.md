# OpenRoom Chat

OpenRoom is a real-time, room-based chat app built with Streamlit and Firebase Authentication + Realtime Database.

## Features
- Email/password sign-up and sign-in, email verification, password reset, and refreshed Firebase sessions
- General, Study room, and Lounge channels with messages that refresh every three seconds
- Moderator console for reviewing and deleting recent messages
- Firebase database rules restrict access to verified accounts, limit message writes to the authenticated author, and reserve deletion for the configured moderator
- Responsive chat layout with reduced-motion support

## Firebase setup
1. Create a Firebase project.
2. In **Authentication → Sign-in method**, enable **Email/Password** and configure the email action templates.
3. Create a **Realtime Database**. Start in locked mode and copy its database URL.
4. Add `firebase.rules.json` to the Realtime Database Rules tab. Replace `moderator@example.com` with the exact verified moderator email. For additional moderators, add corresponding email comparisons to the `.write` rule and list each email in `ADMIN_EMAILS`.
5. In **Project settings → General**, copy the web app API key.
6. Create `.streamlit/secrets.toml` locally (or set the same environment variables in your host):

	```toml
	FIREBASE_API_KEY = "your-firebase-web-api-key"
	FIREBASE_DATABASE_URL = "https://your-project-default-rtdb.region.firebasedatabase.app"
	ADMIN_EMAILS = "moderator@example.com"
	```

7. Install dependencies and run the app:

	```bash
	pip install -r requirements.txt
	streamlit run app.py
	```

`main2.py` is also supported as an entrypoint for the dev container. The Firebase web API key is intended for client applications; database authorization is enforced by Firebase rules. Never add a service-account private key or commit `secrets.toml`.

## Data and moderation

Messages are stored at `rooms/{room}/messages/{messageId}` and the UI fetches at most the latest 100 messages per room. Deletion in the moderator console permanently removes the selected message. This starter app does not include direct messages, image uploads, push notifications, rate limiting, or abuse reporting; add those before opening a community to the public.
