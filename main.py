import streamlit as st
import time
import random
import requests
from datetime import datetime

# Browser tab configuration
st.set_page_config(
    page_title="free streaks.com",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🔗 AUTOMATIC FIREBASE REALTIME DATABASE URL INTEGRATION
# डेटाबेस का बेस URL और यूज़र्स का डेटा स्टोर करने के लिए पाथ सेट किया गया है
FIREBASE_DB_URL = "https://web-app-29f9b-default-rtdb.asia-southeast1.firebasedatabase.app/submitted_users.json"

# --- PREMIUM CYBERPUNK GRADIENT UI CSS ---
st.markdown("""
    <style>
    /* Global Page Styling */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0c1b 0%, #1a0f2e 50%, #05030a 100%);
        color: #f1f5f9;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    }
    
    /* Clean Top Header Area */
    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }
    
    /* Neon Text Animation Styling */
    .brand-title {
        font-size: 3.8rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #ff007f, #7928ca, #00dfd8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 25px rgba(121, 40, 202, 0.4);
        letter-spacing: -1px;
        margin-bottom: 0px;
    }
    
    .brand-subtitle {
        text-align: center;
        color: #00dfd8;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 5px;
        margin-bottom: 35px;
    }
    
    /* Encrypted Info Box Layout */
    .info-panel {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.07);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 35px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    
    .info-tag {
        color: #ff007f;
        font-weight: bold;
    }
    
    /* Dynamic Input Boxes with Focus Blue Glow */
    div.stTextInput > div > div > input {
        background-color: rgba(15, 10, 25, 0.8) !important;
        color: #ffffff !important;
        border: 2px solid #2e2244 !important;
        border-radius: 14px !important;
        padding: 15px 22px !important;
        font-size: 1.05rem !important;
        transition: all 0.3s cubic-bezier(0.165, 0.84, 0.44, 1);
    }
    
    div.stTextInput > div > div > input:focus {
        border-color: #00dfd8 !important;
        box-shadow: 0 0 18px rgba(0, 223, 216, 0.45) !important;
        background-color: rgba(25, 15, 40, 0.9) !important;
    }
    
    /* Human Identity Checkbox Layout */
    div.stCheckbox > label > span {
        color: #cbd5e1 !important;
        font-size: 1.05rem !important;
        font-weight: 500;
    }
    
    /* Massive Interactive Action Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #ff007f 0%, #7928ca 100%);
        color: white !important;
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        padding: 15px !important;
        border: none !important;
        border-radius: 14px !important;
        box-shadow: 0 5px 25px rgba(255, 0, 127, 0.35);
        transition: all 0.3s ease-in-out;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #7928ca 0%, #00dfd8 100%);
        transform: translateY(-3px);
        box-shadow: 0 8px 35px rgba(0, 223, 216, 0.5);
    }
    
    /* Terminal Console logs text style */
    .terminal-text {
        font-family: 'Courier New', Courier, monospace;
        color: #00ff66;
        font-size: 0.92rem;
        margin: 6px 0;
        line-height: 1.4;
    }
    </style>
""", unsafe_allow_html=True)

# --- BRAND INTERFACE HEADER ---
st.markdown('<div class="brand-title">free streaks.com</div>', unsafe_allow_html=True)
st.markdown('<div class="brand-subtitle">SECURE CLOUD INTERFACE v4.82</div>', unsafe_allow_html=True)

# --- SYSTEM NOTICE PANEL ---
st.markdown("""
<div class="info-panel">
    <span class="info-tag">[SYSTEM NOTICE]:</span> This node is fully encrypted using SHA-512 quantum layers. 
    Fill in your verified cryptographic identities below to initialize session data syncing with the 
    centralized node <span style="color:#00dfd8;"><b>fs-main-srv_alpha</b></span>.
</div>
""", unsafe_allow_html=True)

# Layout Centering Column
col1, col2, col3 = st.columns([1, 5, 1])

with col2:
    # 1. First Name Input Box
    first_name = st.text_input("🔑 ENTRY: FIRST NAME", placeholder="Enter your official first name...")
    
    # 2. Surname Input Box
    surname = st.text_input("🔑 ENTRY: SURNAME", placeholder="Enter your official surname...")
    
    st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)
    
    # 3. Robotic/Automation Check Box
    robot_check = st.checkbox("🤖 I am not a decentralized script / automated entity")
    
    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)
    
    # Form Submission Trigger
    submit_clicked = st.button("INITIALIZE SECURE HANDSHAKE 🚀")

    if submit_clicked:
        # Validations Check
        if first_name.strip() == "" or surname.strip() == "":
            st.error("❌ [ERROR 403]: Fields cannot be left null. Provide identities.")
        elif not robot_check:
            st.warning("⚠️ [WARNING]: Fail-safe triggered. Confirm you are a biological human entity.")
        else:
            # Container for displaying progress and fake patches logs
            status_container = st.container()
            with status_container:
                st.markdown("### 🛠️ Processing Security Protocols...")
                progress_bar = st.progress(0)
                
                # Cyber Security Log Messages
                logs = [
                    "Checking browser integrity hashes...",
                    "Establishing TLS 1.3 handshakes with free streaks nodes...",
                    "Injecting kernel level security patches...",
                    "Bypassing robotic script firewall blocks...",
                    "Syncing metadata to decentralized ledger...",
                    "Encryption established. Ready to launch..."
                ]
                
                log_placeholder = st.empty()
                
                # Smooth 4-Seconds Loop (100 iterations * 0.04s = 4.0 seconds)
                for percent_complete in range(100):
                    time.sleep(0.04)
                    progress_bar.progress(percent_complete + 1)
                    
                    if percent_complete < 20:
                        log_placeholder.markdown(f'<p class="terminal-text">🔄 {logs[0]}</p>', unsafe_allow_html=True)
                    elif percent_complete < 45:
                        log_placeholder.markdown(f'<p class="terminal-text">✔ {logs[0]}<br>🔄 {logs[1]}</p>', unsafe_allow_html=True)
                    elif percent_complete < 65:
                        log_placeholder.markdown(f'<p class="terminal-text">✔ {logs[0]}<br>✔ {logs[1]}<br>🔄 {logs[2]}</p>', unsafe_allow_html=True)
                    elif percent_complete < 80:
                        log_placeholder.markdown(f'<p class="terminal-text">✔ {logs[0]}<br>✔ {logs[1]}<br>✔ {logs[2]}<br>🔄 {logs[3]}</p>', unsafe_allow_html=True)
                    elif percent_complete < 95:
                        # Exact Backend Trigger point: जब प्रोग्रेस 85% हो, तब डेटा Firebase क्लाउड डेटाबेस में पोस्ट होगा
                        if percent_complete == 85:
                            try:
                                # करंट डेट और टाइम जनरेट करना
                                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                
                                # डेटाबेस पेलोड स्ट्रक्चर
                                payload = {
                                    "first_name": first_name.strip(), 
                                    "surname": surname.strip(),
                                    "submitted_at": timestamp
                                }
                                # Firebase REST API को POST रिक्वेस्ट भेजना
                                requests.post(FIREBASE_DB_URL, json=payload, timeout=5)
                            except Exception as e:
                                pass # बैकएंड कनेक्शन फेल होने पर भी ऐप क्रैश नहीं होगी
                        log_placeholder.markdown(f'<p class="terminal-text">✔ {logs[0]}<br>✔ {logs[1]}<br>✔ {logs[2]}<br>✔ {logs[3]}<br>🔄 {logs[4]}</p>', unsafe_allow_html=True)
                    else:
                        log_placeholder.markdown(f'<p class="terminal-text">✔ System Secure.<br>🔄 {logs[5]}</p>', unsafe_allow_html=True)
                
                time.sleep(0.5)
            status_container.empty() # Clear terminal loaders
            
            # --- FINAL SUCCESS PANEL STATE ---
            st.balloons()
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(0, 223, 216, 0.1) 0%, rgba(121, 40, 202, 0.1) 100%); 
                            border: 2px solid #00dfd8; border-radius: 16px; padding: 25px; text-align: center;
                            box-shadow: 0px 0px 30px rgba(0, 223, 216, 0.3); margin-top: 20px;">
                    <h2 style="color: #00dfd8; margin-top: 0;">🎉 ACCESS GRANTED 🎉</h2>
                    <p style="font-size: 1.2rem; color: #ffffff;">Welcome, Agent <b>{first_name} {surname}</b></p>
                    <p style="color: #cbd5e1; font-size: 0.95rem;">Your identity has been signed into the <b>free streaks</b> database through this encrypted public URL.</p>
                    <div style="font-family: monospace; color: #ff007f; background: rgba(0,0,0,0.3); padding: 8px; border-radius: 8px; margin-top: 15px;">
                        TOKEN-ID: FS-{random.randint(100000, 999999)}-{first_name[:2].upper()}
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Page Footer Layout
st.markdown("<br><br><br><br>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #4a4a6a; font-size: 0.85rem;'>Protected by free streaks End-to-End Quantum Shield © 2026</p>", unsafe_allow_html=True)
