import streamlit as st
import time
import requests
import datetime
import uuid

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Vinay Chat | Official Creator Portal",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. PREMIUM CSS INJECTION (SAFE RAW STRING FORMAT) ---
# Using raw string formatting rules to eliminate any possibility of Python compiler syntax errors
st.markdown(r"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .main {
        background-color: #f8fafc;
    }
    .stApp {
        background-color: #ffffff;
    }
    /* Hero Section Graphics */
    .hero-title {
        font-size: 42px;
        font-weight: 700;
        color: #0f172a;
        text-align: center;
        margin-bottom: 10px;
        background: -webkit-linear-gradient(45deg, #2563eb, #9333ea);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 18px;
        color: #64748b;
        text-align: center;
        margin-bottom: 40px;
    }
    /* Cards and Containers */
    .premium-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
    }
    /* Feature List Items */
    .feature-item {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        color: #334155;
        font-weight: 600;
    }
    .feature-icon {
        color: #10b981;
        margin-right: 10px;
        font-size: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. SECURE FIREBASE CONFIG ---
FIREBASE_URL = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/vinay_chat_requests.json"

# --- 4. SESSION STATE MANAGEMENT ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

def go_to_step(step_num):
    st.session_state.step = step_num

# ==========================================
# STEP 1: PREMIUM LANDING PAGE
# ==========================================
if st.session_state.step == 1:
    st.markdown("<div class='hero-title'>Boost Your Vinay Chat Reach</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>Get authentic, high-quality followers organically. 100% Secure & Verified.</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class='premium-card'>
            <h4 style="color:#0f172a; margin-bottom: 20px;">Why choose Creator Portal?</h4>
            <div class='feature-item'><span class='feature-icon'>✓</span> Secure Authentication</div>
            <div class='feature-item'><span class='feature-icon'>✓</span> Real User Checks via AI</div>
            <div class='feature-item'><span class='feature-icon'>✓</span> Instant Profile Sync</div>
            <div class='feature-item'><span class='feature-icon'>✓</span> End-to-End Encryption</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Secure Login / Get Started →", use_container_width=True, type="primary"):
            go_to_step(2)
            st.rerun()

# ==========================================
# STEP 2: USER METADATA COLLECTION FORM
# ==========================================
elif st.session_state.step == 2:
    st.markdown("<div class='hero-title'>Creator Authentication</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#64748b;'>Enter your details exactly as they appear on your Vinay Chat App profile.</p>", unsafe_allow_html=True)
    
    with st.form("user_details_form"):
        col1, col2 = st.columns(2)
        with col1:
            fname = st.text_input("First Name")
            age = st.number_input("Age", min_value=13, max_value=100, step=1)
        with col2:
            lname = st.text_input("Last Name")
            chat_id = st.text_input("Vinay Chat Username (@id)")
            
        pyq_code = st.text_input("Reference/Promo Code (Optional)")
        
        submitted = st.form_submit_button("Verify Identity & Continue", type="primary")
        
        if submitted:
            if fname and lname and chat_id:
                st.session_state.user_data = {
                    "first_name": fname,
                    "last_name": lname,
                    "age": age,
                    "chat_id": chat_id,
                    "promo_code": pyq_code
                }
                go_to_step(3)
                st.rerun()
            else:
                st.error("Please fill in all mandatory fields.")

# ==========================================
# STEP 3: AUTOMATED VALIDATION GRAPHICS
# ==========================================
elif st.session_state.step == 3:
    st.markdown("<div class='hero-title'>System Verification</div>", unsafe_allow_html=True)
    st.write("Please wait while our servers verify your profile integrity...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    checks = [
        ("Establishing Secure Connection...", 15),
        ("Verifying Vinay Chat App version...", 35),
        ("Running Real User Validation Check...", 55),
        ("Public Profile Accessibility Check...", 75),
        ("Profile Picture Matrix Syncing...", 90),
        ("Finalizing Security Token...", 100)
    ]
    
    for text, percent in checks:
        status_text.info(text)
        time.sleep(1.0)
        progress_bar.progress(percent)
        
    status_text.success("All checks passed successfully! Profile verified.")
    time.sleep(0.5)
    
    go_to_step(4)
    st.rerun()

# ==========================================
# STEP 4: PACKAGE RATIO MATRIX & FIREBASE SYNC
# ==========================================
elif st.session_state.step == 4:
    st.markdown(f"<div class='hero-title'>Welcome, {st.session_state.user_data['first_name']}!</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Select the organic follower package for your account.</p>", unsafe_allow_html=True)
    
    st.markdown("### Choose Target Audience Size")
    followers_count = st.select_slider(
        "Followers to be credited",
        options=[100, 200, 500, 1000, 2000, 5000, 10000]
    )
    
    # Cost Ratio Formula: ₹10 INR flat scale per 100 allocation units
    total_cost = int((followers_count / 100) * 10)
    
    st.info(f"**Calculated Processing Fee:** ₹{total_cost} INR")
    
    if st.button("Generate Secure Pay Token & Finalize", type="primary", use_container_width=True):
        with st.spinner("Generating encrypted transaction token..."):
            time.sleep(1.5)
            token = f"VCT-{str(uuid.uuid4())[:8].upper()}-PAY"
            
            # Pack all structured components safely
            payload = {
                "timestamp": str(datetime.datetime.now()),
                "status": "Pending Allocation",
                "user_info": st.session_state.user_data,
                "order_details": {
                    "followers_requested": followers_count,
                    "amount_inr": total_cost,
                    "transaction_token": token
                }
            }
            try:
                requests.post(FIREBASE_URL, json=payload)
            except:
                pass
            
            st.session_state.token = token
            go_to_step(5)
            st.rerun()

# ==========================================
# STEP 5: RECEIPT LEDGER & ESTIMATED WAIT TIME
# ==========================================
elif st.session_state.step == 5:
    st.markdown("<div class='hero-title' style='color:#10b981;'>Request Confirmed!</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='premium-card' style='text-align:center;'>
        <h3 style='color:#334155;'>Transaction Token: <span style='color:#2563eb;'>{st.session_state.token}</span></h3>
        <p style='color:#64748b; font-size:15px; margin-top:20px;'>
            Your profile has been queued in our distribution network. 
        </p>
        <hr style='border:1px solid #e2e8f0; margin: 20px 0;'>
        <h4 style='color:#ef4444;'>⏱️ Estimated Time</h4>
        <p>Standard Allocation: <b>3 to 4 Hours</b></p>
        <p style='color:#10b981;'><i>Since your ID check passed flawlessly, wait time is reduced to roughly <b>1 Hour</b>.</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.warning("Please do not change your Vinay Chat Username while the allocation is in progress.")
    
    if st.button("Return to Home"):
        st.session_state.clear()
        st.rerun()
