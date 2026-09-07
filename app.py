import streamlit as st
import json
import hashlib
import os
import datetime
from PIL import Image
import google.generativeai as genai

st.set_page_config(
    page_title="SheSafe - Cyber Defense & Redress",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

* {
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Background */
.stApp {
    background: radial-gradient(circle at 50% 15%, #1e1338 0%, #0f0a1c 60%, #08060f 100%);
    color: #f1f5f9;
}

/* Top Emergency Ribbon */
.emergency-ribbon {
    background: rgba(26, 16, 48, 0.85);
    border: 1px solid rgba(168, 85, 247, 0.25);
    backdrop-filter: blur(8px);
    border-radius: 10px;
    padding: 10px 24px;
    display: flex;
    justify-content: space-between;
    font-size: 0.85rem;
    color: #c4b5fd;
    margin-bottom: 2rem;
}
.emergency-ribbon span.highlight {
    color: #f472b6;
    font-weight: 700;
}

/* Hero Section */
.hero-wrapper {
    text-align: center;
    margin-bottom: 2rem;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #ffffff 40%, #e879f9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.4rem;
}
.hero-subtitle {
    font-size: 0.95rem;
    color: #cbd5e1;
    font-weight: 400;
}

/* Assurance Banner */
.reassurance-banner {
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.15) 0%, rgba(244, 114, 182, 0.15) 100%);
    border: 1px solid rgba(244, 114, 182, 0.3);
    border-radius: 14px;
    padding: 16px 20px;
    text-align: center;
    margin-bottom: 1.8rem;
}
.reassurance-quote {
    font-size: 1.05rem;
    font-weight: 700;
    color: #fdf2f8;
}
.reassurance-sub {
    font-size: 0.8rem;
    color: #e9d5ff;
    margin-top: 4px;
}

/* Authentication Card Styling */
div[data-testid="stForm"] {
    background: rgba(22, 13, 41, 0.85) !important;
    border: 1px solid rgba(168, 85, 247, 0.35) !important;
    border-radius: 18px !important;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5) !important;
    padding: 2rem !important;
}

/* Mandatory input labels */
div[data-testid="stTextInput"] label {
    color: #e2e8f0 !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
}
div[data-testid="stTextInput"] input {
    background-color: rgba(15, 10, 28, 0.9) !important;
    color: #ffffff !important;
    border: 1px solid rgba(168, 85, 247, 0.3) !important;
    border-radius: 8px !important;
}

/* Distinct, high-contrast action buttons */
div.stButton > button:first-child, div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%) !important;
    color: #ffffff !important;
    border: 1px solid #f472b6 !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.2rem !important;
    box-shadow: 0 4px 15px rgba(236, 72, 153, 0.35) !important;
}
div.stButton > button:first-child:hover, div[data-testid="stFormSubmitButton"] > button:hover {
    box-shadow: 0 6px 20px rgba(236, 72, 153, 0.55) !important;
    transform: translateY(-1px) !important;
}

/* Quick Action Cards */
.action-box {
    background: rgba(24, 15, 45, 0.7);
    border: 1px solid rgba(168, 85, 247, 0.2);
    border-radius: 12px;
    padding: 14px;
    text-align: center;
}
.action-title {
    font-size: 0.82rem;
    font-weight: 700;
    color: #f1f5f9;
}
.action-desc {
    font-size: 0.72rem;
    color: #a855f7;
    margin-top: 2px;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# File Persistence
USERS_DB = "users_vault.json"
INCIDENTS_DB = "incidents_vault.json"

def hash_pass(pwd: str) -> str:
    return hashlib.sha256(pwd.encode()).hexdigest()

def get_db(f):
    if os.path.exists(f):
        try:
            with open(f, "r") as fp:
                return json.load(fp)
        except Exception:
            return {}
    return {}

def put_db(f, d):
    with open(f, "w") as fp:
        json.dump(d, fp, indent=2)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None

# Top Ribbon
st.markdown("""
<div class="emergency-ribbon">
    <div>Women Safety Helpline: <span class="highlight">181</span> | Police Emergency: <span class="highlight">112</span></div>
    <div>National Cybercrime Portal: <span class="highlight">1930</span> (cybercrime.gov.in)</div>
</div>
""", unsafe_allow_html=True)

# Unauthenticated State
if not st.session_state.authenticated:
    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero-title">SheSafe Cyber Defense Vault</div>
        <div class="hero-subtitle">Tamper-evident legal incident intake and statutory analysis</div>
    </div>
    """, unsafe_allow_html=True)

    col_space_l, col_main, col_space_r = st.columns([1, 1.4, 1])

    with col_main:
        st.markdown("""
        <div class="reassurance-banner">
            <div class="reassurance-quote">"Brave girls make safer tomorrows."</div>
            <div class="reassurance-sub">Help is always within reach. You are never alone.</div>
        </div>
        """, unsafe_allow_html=True)

        tab_sign, tab_reg = st.tabs(["Secure Sign In", "Create Vault Account"])

        with tab_sign:
            with st.form("form_signin"):
                u_in = st.text_input("Case Identifier or Username", placeholder="e.g., yuvika1234").strip()
                p_in = st.text_input("Access Password", type="password", placeholder="Enter verified passphrase").strip()
                submit_sign = st.form_submit_button("Access Safety Shield", use_container_width=True)

                if submit_sign:
                    if not u_in or not p_in:
                        st.error("Authentication required: Please enter both username and password.")
                    else:
                        users = get_db(USERS_DB)
                        if u_in in users and users[u_in] == hash_pass(p_in):
                            st.session_state.authenticated = True
                            st.session_state.username = u_in
                            st.rerun()
                        else:
                            st.error("Access denied: Invalid credentials.")

        with tab_reg:
            with st.form("form_register"):
                reg_u = st.text_input("Choose Username / Identifier").strip()
                reg_p = st.text_input("Choose Secure Password", type="password").strip()
                reg_c = st.text_input("Confirm Password", type="password").strip()
                submit_reg = st.form_submit_button("Create Private Vault", use_container_width=True)

                if submit_reg:
                    if not reg_u or not reg_p:
                        st.error("All credential fields are mandatory.")
                    elif reg_p != reg_c:
                        st.error("Passwords do not match.")
                    else:
                        users = get_db(USERS_DB)
                        if reg_u in users:
                            st.warning("Identifier already registered.")
                        else:
                            users[reg_u] = hash_pass(reg_p)
                            put_db(USERS_DB, users)
                            st.success("Account registered. You may now sign in.")

# Authenticated State
else:
    col_hdr, col_btn = st.columns([4, 1])
    with col_hdr:
        st.subheader(f"Active Case Vault: {st.session_state.username}")
    with col_btn:
        if st.button("Sign Out", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.username = None
            st.rerun()

    st.markdown("---")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="action-box"><div class="action-title">Live Tracking</div><div class="action-desc">Family Sharing</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="action-box"><div class="action-title">Contacts</div><div class="action-desc">Emergency Network</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="action-box"><div class="action-title">Safe Spots</div><div class="action-desc">Nearby Help</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="action-box"><div class="action-title">Incident Desk</div><div class="action-desc">Evidence Logging</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab_intake, tab_archive = st.tabs(["Forensic Incident Intake", "Preserved Vault"])

    with tab_intake:
        st.markdown("##### Digital Incident Submission")
        ev_text = st.text_area("Evidence Text, Transcripts, or Threat URLs", height=130)
        ev_file = st.file_uploader("Upload Screenshots / File Artifacts", type=["png", "jpg", "jpeg"])

        if st.button("Run AI Forensic Assessment", use_container_width=True):
            if not ev_text and not ev_file:
                st.error("Please supply evidence text or upload an artifact to process.")
            else:
                with st.spinner("Computing SHA-256 hash and analyzing legal statutes..."):
                    payload = ev_text
                    img = None
                    if ev_file:
                        img = Image.open(ev_file)
                        payload += f" [File: {ev_file.name}]"

                    computed_hash = hashlib.sha256(payload.encode()).hexdigest()

                    try:
                        api_key = os.environ.get("GEMINI_API_KEY")
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel("gemini-2.5-flash")

                        prompt = f"""
                        You are a certified cyber legal and digital forensics expert specializing in Indian Cyber Law and women's cyber defense.
                        Analyze the following cyber incident evidence:
                        Evidence: {ev_text}

                        Provide a structured forensic report containing:
                        1. Threat Assessment & Risk Level (Critical, High, Medium, Low)
                        2. Applicable Legal Statutes under Information Technology Act, 2000 (e.g., Section 66E, 67, 67A) and Bharatiya Nyaya Sanhita, 2023 (e.g., Section 78, 79, 351).
                        3. Immediate Digital Safety Steps.
                        4. Formal Police/Cyber Cell Complaint Draft ready for official filing.
                        Do not use conversational filler or emojis.
                        """

                        contents = [prompt]
                        if img:
                            contents.append(img)

                        response = model.generate_content(contents)
                        report_out = response.text

                        incidents = get_db(INCIDENTS_DB)
                        if st.session_state.username not in incidents:
                            incidents[st.session_state.username] = []

                        incidents[st.session_state.username].append({
                            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
                            "sha256": computed_hash,
                            "report": report_out
                        })
                        put_db(INCIDENTS_DB, incidents)

                        st.success("Evidence cryptographically registered in vault.")
                        st.code(f"SHA-256 Hash: {computed_hash}", language="text")
                        st.markdown(report_out)

                    except Exception as e:
                        st.error(f"Analysis error: {str(e)}")

    with tab_archive:
        st.markdown("##### Cryptographic Chain of Custody")
        incidents = get_db(INCIDENTS_DB)
        records = incidents.get(st.session_state.username, [])
        if not records:
            st.info("No records currently preserved in this vault.")
        else:
            for i, r in enumerate(reversed(records), 1):
                with st.expander(f"Incident #{i} - {r['timestamp']}"):
                    st.code(f"SHA-256: {r['sha256']}", language="text")
                    st.markdown(r['report'])
