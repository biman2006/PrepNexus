import streamlit as st
import tempfile
import os
import re
import time
import json
from PIL import Image
import importlib
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

# =====================================================
# VECTORSTORE IMPORT HELPER
# =====================================================
def _import_faiss():
    for mod_name in ("langchain_community.vectorstores", "langchain.vectorstores"):
        try:
            mod = importlib.import_module(mod_name)
            return getattr(mod, "FAISS")
        except Exception:
            continue
    return None

FAISS = _import_faiss()

# =====================================================
# BACKEND IMPORTS
# =====================================================
from utils.pdf_parser import extract_text_from_pdf
from utils.text_cleaner import clean_text
from utils.skill_extractor import extract_skill, normalize_skill
from utils.readiness_scorer import calculate_readiness

from rag.embedder import load_embeddings
from data.all_skills import all_skills
from data.role_weights import role_skill_weights

from utils.pdf_exporter import generate_resume_pdf
from utils.auth import (
    hash_password,
    is_strong_password,
    create_jwt_token,
    decode_jwt_token,
    verify_jwt_session,
    get_jwt_token_claims,
)
from utils.structured_output import (
    format_structured_resume_plain_text,
    calculate_resume_ats_score,
)
from utils.resume_api_builder import (
    generate_resume,
    generate_ai_summary,
    enhance_bullet_point,
    suggest_role_keywords,
    build_local_structured_resume,
)

from database.crud import (
    get_user_by_email,
    get_user_by_id,
    register_user,
    authenticate_user,
    save_resume,
    get_user_resumes,
)
from database.init_db import initialize_database
from utils.gemini_config import gemini_model, get_configured_gemini_model

# Services
try:
    from recomendation.recomendation_engine import RecomendationEngine
except Exception as e:
    RecomendationEngine = None

from chatbot.chatbot_service import PrepNexusChatbot
from admin.admin_ui import show_admin_panel

# =====================================================
# PAGE CONFIGURATION
# =====================================================
icon_path = "assets/icon.png"
logo_path = "assets/logo.png"
icon = Image.open(icon_path) if os.path.exists(icon_path) else None
logo = Image.open(logo_path) if os.path.exists(logo_path) else None

st.set_page_config(
    page_title="PrepNexus | AI Career & ATS Intelligence",
    page_icon=icon or "🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LUXURY DARK GLASSMORPHISM DESIGN SYSTEM
# =====================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Background & Core Layout */
.stApp {
    background: radial-gradient(circle at 10% 20%, rgba(30, 58, 138, 0.25) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(13, 148, 136, 0.2) 0%, transparent 45%),
                linear-gradient(180deg, #090D16 0%, #0F172A 100%);
    color: #F8FAFC;
}

/* Glassmorphic Container Cards */
.glass-card {
    background: rgba(17, 24, 39, 0.65);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.4);
    transition: transform 0.2s ease, border-color 0.2s ease;
}
.glass-card:hover {
    border-color: rgba(99, 102, 241, 0.35);
}

/* Header Banner */
.hero-banner {
    background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.85) 100%);
    border: 1px solid rgba(99, 102, 241, 0.25);
    border-radius: 20px;
    padding: 30px 40px;
    margin-bottom: 25px;
    box-shadow: 0 12px 35px -8px rgba(0, 0, 0, 0.5);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, #6366F1, #06B6D4, #10B981);
}

/* Metric Display Cards */
.metric-box {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 16px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}
.metric-box .metric-val {
    font-size: 32px;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.5px;
}
.metric-box .metric-lbl {
    font-size: 13px;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 4px;
}

/* Skill Badges & Chips */
.badge-matched {
    display: inline-block;
    background: rgba(16, 185, 129, 0.15);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 600;
    margin: 4px;
}
.badge-missing {
    display: inline-block;
    background: rgba(239, 68, 68, 0.15);
    color: #F87171;
    border: 1px solid rgba(239, 68, 68, 0.3);
    padding: 6px 14px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 600;
    margin: 4px;
}
.badge-category {
    display: inline-block;
    background: rgba(99, 102, 241, 0.15);
    color: #A5B4FC;
    border: 1px solid rgba(99, 102, 241, 0.3);
    padding: 5px 12px;
    border-radius: 9999px;
    font-size: 12px;
    font-weight: 600;
    margin: 3px;
}

/* Modern Input & Button Enhancements */
.stButton > button {
    border-radius: 12px;
    font-weight: 700;
    background: linear-gradient(135deg, #4F46E5 0%, #2563EB 100%);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35);
    transition: all 0.2s ease-in-out;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5);
    border-color: rgba(255, 255, 255, 0.3);
}

/* Secondary Button Styling */
button[kind="secondary"] {
    background: rgba(30, 41, 59, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #F8FAFC !important;
}

/* Tab Styling */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(15, 23, 42, 0.6);
    padding: 6px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.06);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    font-weight: 600;
    color: #94A3B8;
    padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    background: #4F46E5 !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.35);
}

/* Form Inputs */
.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background-color: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 10px !important;
    color: #F8FAFC !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: #6366F1 !important;
    box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.25) !important;
}

/* Chat Message Card */
.chat-bubble-user {
    background: rgba(79, 70, 229, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 16px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.chat-bubble-bot {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 18px 22px;
    margin-bottom: 14px;
}

/* JWT Security Badge in Sidebar */
.jwt-pill {
    display: inline-flex;
    align-items: center;
    background: rgba(16, 185, 129, 0.12);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #10B981;
    font-size: 11px;
    font-weight: 700;
    padding: 4px 10px;
    border-radius: 9999px;
    letter-spacing: 0.4px;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE & JWT BOOTSTRAP
# =====================================================
def init_session():
    defaults = {
        "logged_in": False,
        "jwt_token": "",
        "user_id": None,
        "user_email": "",
        "user_name": "",
        "user_role": "user",
        "resume_builder_data": None,
        "resume_builder_ats": None,
        "last_generated_plain": "",
        "chat_history": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()
initialize_database()

# Check Query Params for JWT session persistence (e.g. on page refresh or direct link)
query_token = st.query_params.get("token")
if not st.session_state.logged_in and query_token:
    verified = verify_jwt_session(query_token)
    if verified:
        st.session_state.logged_in = True
        st.session_state.jwt_token = query_token
        st.session_state.user_id = verified["user_id"]
        st.session_state.user_email = verified["email"]
        st.session_state.user_name = verified["name"]
        st.session_state.user_role = verified["role"]
    else:
        # Invalid or expired token in query param
        st.query_params.clear()

def is_admin():
    user_id = st.session_state.get("user_id")
    if not st.session_state.get("logged_in") or not user_id:
        return False
    user = get_user_by_id(user_id)
    return bool(user and user.is_active and user.role == "admin")

# =====================================================
# DISPLAY SKILL FORMATTER
# =====================================================
def display_skill(skill: str) -> str:
    s = skill.strip().lower()
    mapping = {
        "c++": "C++", "c#": "C#", "dotnet": ".NET",
        "javascript": "JavaScript", "typescript": "TypeScript",
        "python": "Python", "sql": "SQL", "mysql": "MySQL", "postgresql": "PostgreSQL",
        "mongodb": "MongoDB", "redis": "Redis", "docker": "Docker", "kubernetes": "Kubernetes",
        "aws": "AWS", "gcp": "GCP", "azure": "Azure", "ci cd": "CI/CD",
        "react": "React", "react.js": "React.js", "next.js": "Next.js",
        "node.js": "Node.js", "fastapi": "FastAPI", "flask": "Flask", "django": "Django",
        "scikit learn": "Scikit-Learn", "tensorflow": "TensorFlow", "pytorch": "PyTorch",
        "power bi": "Power BI", "tableau": "Tableau", "rest api": "REST API",
        "git": "Git", "github": "GitHub", "system design": "System Design",
    }
    return mapping.get(s, " ".join(word.capitalize() for word in s.split()))

available_roles = sorted(list(role_skill_weights.keys()))

# =====================================================
# LOGIN & REGISTER VIEW
# =====================================================
def login_page():
    col1, col2, col3 = st.columns([1, 2.2, 1])

    with col2:
        if logo:
            st.image(logo, width=420)
        else:
            st.markdown("<h1 style='color:#6366F1;'>🎯 PrepNexus</h1>", unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">
            <h2 style="margin: 0; color: #FFFFFF; font-size: 26px;">🔐 Candidate Portal</h2>
            <p style="color: #94A3B8; font-size: 14px; margin-top: 4px;">
                Secure JWT-authenticated Career & ATS Intelligence System
            </p>
        </div>
        """, unsafe_allow_html=True)

        auth_mode = st.radio("Authentication Mode", ["Login", "Create Account"], horizontal=True)

        name = ""
        if auth_mode == "Create Account":
            name = st.text_input("Full Name", placeholder="e.g. Jane Doe")

        email = st.text_input("Email Address", placeholder="name@domain.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")

        confirm_password = ""
        if auth_mode == "Create Account":
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="••••••••")
            st.caption("🔒 Password must be at least 8 characters and include uppercase, lowercase, and numbers.")

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

        if st.button("🚀 Access PrepNexus Platform", use_container_width=True):
            normalized_email = email.strip().lower()

            if not email.strip():
                st.warning("Please enter your email.")
            elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', normalized_email):
                st.warning("Please enter a valid email address.")
            elif not password:
                st.warning("Please enter your password.")
            elif auth_mode == "Create Account" and not name.strip():
                st.warning("Please provide your full name.")
            elif auth_mode == "Create Account" and password != confirm_password:
                st.warning("Passwords do not match.")
            elif auth_mode == "Create Account" and not is_strong_password(password):
                st.warning("Password does not meet strength requirements.")
            else:
                existing_user = get_user_by_email(normalized_email)

                if auth_mode == "Create Account":
                    if existing_user:
                        st.warning("Account already exists. Please select Login.")
                    else:
                        password_hash = hash_password(password)
                        user = register_user(name, normalized_email, password_hash)
                        if user:
                            # Generate JWT Token
                            token = create_jwt_token(user.id, user.email, user.name, user.role)
                            st.session_state.logged_in = True
                            st.session_state.jwt_token = token
                            st.session_state.user_id = user.id
                            st.session_state.user_email = user.email
                            st.session_state.user_name = user.name
                            st.session_state.user_role = user.role
                            st.query_params["token"] = token
                            st.success("✅ Account created and authenticated successfully!")
                            time.sleep(0.8)
                            st.rerun()
                        else:
                            st.error("Failed to create account. Please try again.")

                elif auth_mode == "Login":
                    if not existing_user:
                        st.error("Invalid credentials.")
                    else:
                        user = authenticate_user(normalized_email, password)
                        if user:
                            # Generate JWT Token
                            token = create_jwt_token(user.id, user.email, user.name, user.role)
                            st.session_state.logged_in = True
                            st.session_state.jwt_token = token
                            st.session_state.user_id = user.id
                            st.session_state.user_email = user.email
                            st.session_state.user_name = user.name or ""
                            st.session_state.user_role = user.role
                            st.query_params["token"] = token
                            st.success("🎉 Authentication verified!")
                            time.sleep(0.8)
                            st.rerun()
                        else:
                            st.error("Invalid email or password.")

    st.stop()

# =====================================================
# SIDEBAR
# =====================================================
def render_sidebar():
    with st.sidebar:
        if logo:
            st.image(logo, width=220)
        else:
            st.markdown("## 🎯 PrepNexus")

        # User profile chip
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.08); padding: 14px; border-radius: 14px; margin-bottom: 14px;">
            <div style="font-weight: 700; color: #FFFFFF; font-size: 15px;">👤 {st.session_state.user_name or 'Candidate'}</div>
            <div style="color: #94A3B8; font-size: 12px; margin-top: 2px;">{st.session_state.user_email}</div>
            <div class="jwt-pill">🛡️ JWT AUTHENTICATED</div>
        </div>
        """, unsafe_allow_html=True)

        # JWT Token Inspection
        token = st.session_state.get("jwt_token")
        if token:
            claims = get_jwt_token_claims(token)
            with st.expander("🔑 Session JWT Claims"):
                st.caption(f"**Expires:** {claims.get('expires_at')}")
                st.caption(f"**TTL:** {claims.get('time_remaining')}")
                st.caption(f"**Role:** {claims.get('role')}")
                st.caption(f"**Issuer:** {claims.get('issuer')}")
                st.code(token, language="text")
                st.caption("Use this Bearer token for authorized REST API calls.")

        st.markdown("---")

        # Navigation mode
        if is_admin():
            nav = st.radio("Navigation", ["User Workspace", "Admin Console"], horizontal=True)
        else:
            nav = "User Workspace"

        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state.clear()
            st.query_params.clear()
            st.rerun()

        return nav

# =====================================================
# APP HEADER
# =====================================================
def render_header():
    resumes = get_user_resumes(st.session_state.user_email)
    latest_score = next((r.readiness_score for r in reversed(resumes) if r.readiness_score is not None), None)

    st.markdown(f"""
    <div class="hero-banner">
        <h1 style="color: #FFFFFF; font-size: 32px; font-weight: 800; margin: 0 0 8px 0; letter-spacing: -0.5px;">
            🚀 PrepNexus Career Intelligence
        </h1>
        <p style="color: #94A3B8; font-size: 16px; margin: 0; max-width: 800px;">
            Analyze resumes against real hiring standards, build high-impact ATS-optimized resumes, and bridge skill gaps with AI recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-val">{len(resumes)}</div>
            <div class="metric-lbl">Saved Resumes</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        score_display = f"{latest_score:.0f}%" if latest_score is not None else "Pending"
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-val">{score_display}</div>
            <div class="metric-lbl">Latest Readiness Score</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        role_label = "Administrator" if is_admin() else "Candidate Pro"
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-val">{role_label}</div>
            <div class="metric-lbl">Account Tier</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# =====================================================
# TAB 1: RESUME ANALYZER
# =====================================================
def render_resume_analyzer():
    st.markdown("### 📄 Diagnostic Resume & ATS Gap Analysis")
    st.markdown("Upload your current resume in PDF format and choose your target job role to generate a comprehensive gap report.")

    col_up, col_role = st.columns([1.5, 1])
    with col_up:
        uploaded_pdf = st.file_uploader("Upload PDF Resume", type=["pdf"])
    with col_role:
        target_role = st.selectbox("Target Career Track", available_roles, index=0)

    if st.button("🔍 Run Intelligent Diagnostic Analysis", use_container_width=True):
        if uploaded_pdf is None:
            st.warning("Please upload a PDF resume to analyze.")
            return

        with st.spinner("Extracting text and performing multi-vector skill matching..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_pdf.getvalue())
                tmp_path = tmp_file.name

            try:
                raw_text = extract_text_from_pdf(tmp_path)
                cleaned_text = clean_text(raw_text)
                resume_skills = set(normalize_skill(s) for s in extract_skill(cleaned_text, all_skills))

                # Role profile expectations
                role_weights = role_skill_weights.get(target_role.strip().lower(), {})
                core_expected = set(normalize_skill(s) for s in role_weights.get("core", []))
                sec_expected = set(normalize_skill(s) for s in role_weights.get("secondary", []))
                adv_expected = set(normalize_skill(s) for s in role_weights.get("advanced", []))
                total_expected = core_expected.union(sec_expected).union(adv_expected)

                matched_skills = total_expected.intersection(resume_skills)
                missing_skills = total_expected - resume_skills

                # Weighted readiness calculation
                weighted_calc = calculate_readiness(resume_skills, role_weights)
                readiness_score = weighted_calc["readiness_score"]
                ats_match_rate = (len(matched_skills) / len(total_expected) * 100) if total_expected else 0.0

                # Render Results
                st.success("✅ Diagnostic Complete!")

                s1, s2, s3 = st.columns(3)
                with s1:
                    st.metric("ATS Keyword Match", f"{ats_match_rate:.1f}%")
                    st.progress(int(min(100, ats_match_rate)))
                with s2:
                    st.metric("Career Readiness Score", f"{readiness_score:.1f}%")
                    st.progress(int(min(100, readiness_score)))
                with s3:
                    verdict = "Highly Competitive" if readiness_score >= 80 else ("Job Ready" if readiness_score >= 65 else "Skill Gap Detected")
                    st.metric("Hiring Assessment", verdict)

                st.markdown("---")

                # Skill Category Breakdown
                st.subheader("📊 Skill Matrix Breakdown")
                c_core, c_sec, c_adv = st.columns(3)

                with c_core:
                    st.markdown("""
                    <div class="glass-card" style="border-top: 4px solid #EF4444;">
                        <h4 style="margin: 0 0 10px 0; color: #FCA5A5;">🧠 Core Foundations</h4>
                    """, unsafe_allow_html=True)
                    st.caption(f"{len(weighted_calc['core_matched'])} of {len(core_expected)} mastered")
                    st.write("**Matched:**")
                    if weighted_calc["core_matched"]:
                        for s in sorted(weighted_calc["core_matched"]):
                            st.markdown(f"<span class='badge-matched'>✔️ {display_skill(s)}</span>", unsafe_allow_html=True)
                    else:
                        st.caption("No core skills detected.")
                    st.write("**Missing:**")
                    if weighted_calc["missing_core"]:
                        for s in sorted(weighted_calc["missing_core"]):
                            st.markdown(f"<span class='badge-missing'>❌ {display_skill(s)}</span>", unsafe_allow_html=True)
                    else:
                        st.caption("All core skills covered!")
                    st.markdown("</div>", unsafe_allow_html=True)

                with c_sec:
                    st.markdown("""
                    <div class="glass-card" style="border-top: 4px solid #8B5CF6;">
                        <h4 style="margin: 0 0 10px 0; color: #C4B5FD;">⚙️ Secondary Skills</h4>
                    """, unsafe_allow_html=True)
                    st.caption(f"{len(weighted_calc['secondary_matched'])} of {len(sec_expected)} mastered")
                    st.write("**Matched:**")
                    if weighted_calc["secondary_matched"]:
                        for s in sorted(weighted_calc["secondary_matched"]):
                            st.markdown(f"<span class='badge-matched'>✔️ {display_skill(s)}</span>", unsafe_allow_html=True)
                    else:
                        st.caption("None detected.")
                    st.write("**Missing:**")
                    if weighted_calc["missing_secondary"]:
                        for s in sorted(weighted_calc["missing_secondary"]):
                            st.markdown(f"<span class='badge-missing'>❌ {display_skill(s)}</span>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with c_adv:
                    st.markdown("""
                    <div class="glass-card" style="border-top: 4px solid #10B981;">
                        <h4 style="margin: 0 0 10px 0; color: #6EE7B7;">🔬 Advanced Skills</h4>
                    """, unsafe_allow_html=True)
                    st.caption(f"{len(weighted_calc['advanced_matched'])} of {len(adv_expected)} mastered")
                    st.write("**Matched:**")
                    if weighted_calc["advanced_matched"]:
                        for s in sorted(weighted_calc["advanced_matched"]):
                            st.markdown(f"<span class='badge-matched'>✔️ {display_skill(s)}</span>", unsafe_allow_html=True)
                    else:
                        st.caption("None detected.")
                    st.write("**Missing:**")
                    if weighted_calc["missing_advanced"]:
                        for s in sorted(weighted_calc["missing_advanced"]):
                            st.markdown(f"<span class='badge-missing'>❌ {display_skill(s)}</span>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                # AI Recommendations for Missing Skills
                if missing_skills and RecomendationEngine is not None and gemini_model is not None:
                    st.markdown("---")
                    st.subheader("🎯 Targeted AI Upskilling Recommendations")
                    engine = RecomendationEngine(gemini_model)
                    recs = engine.generate_recomendations(list(missing_skills)[:3])

                    for skill, rdata in recs.items():
                        with st.expander(f"📘 Upskilling Blueprint: {display_skill(skill)}", expanded=True):
                            r1, r2 = st.columns(2)
                            with r1:
                                st.write("**📹 Video Tutorials & Playlists:**")
                                if rdata.get("videos"):
                                    for v in rdata["videos"][:3]:
                                        st.markdown(f"- [{v.title}]({v.url})")
                                else:
                                    st.caption("No video links available.")

                                st.write("**🎓 Recommended Courses:**")
                                if rdata.get("courses"):
                                    for c in rdata["courses"][:2]:
                                        st.markdown(f"- [{c.get('title', 'Online Course')}]({c.get('url', '#')})")
                                        if c.get("content"):
                                            st.caption(c["content"][:120] + "...")
                                else:
                                    st.caption("No direct course links found.")

                            with r2:
                                st.write("**🗺️ Learning Roadmap Milestones:**")
                                r_struct = rdata.get("roadmap_structured")
                                if r_struct and isinstance(r_struct, dict):
                                    st.markdown(f"*{r_struct.get('overview', '')}*")
                                    for m_list in [r_struct.get("core_milestones", []), r_struct.get("secondary_milestones", []), r_struct.get("advanced_milestones", [])]:
                                        for m in m_list:
                                            st.markdown(f"- **{m.get('title', 'Milestone')}**: {', '.join(m.get('topics', []))}")
                                else:
                                    st.write(rdata.get("roadmap", "Step-by-step roadmap unavailable."))

            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

# =====================================================
# TAB 2: UPGRADED ATS RESUME BUILDER
# =====================================================
def render_resume_builder():
    st.markdown("### 📝 Professional ATS Resume Architect")
    st.markdown("Build an executive-grade, ATS-compliant resume with live scoring, keyword suggestions, and multi-template PDF exports.")

    builder_mode = st.radio("Select Builder Mode", ["🌟 Interactive Pro Builder", "⚡ Instant AI Auto-Generate"], horizontal=True)

    if builder_mode == "🌟 Interactive Pro Builder":
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        
        # Section 1: Contact Details
        st.subheader("1. Candidate Information")
        c1, c2, c3 = st.columns(3)
        with c1:
            b_name = st.text_input("Full Name", value=st.session_state.user_name or "Jane Doe")
            b_email = st.text_input("Email", value=st.session_state.user_email)
        with c2:
            b_phone = st.text_input("Phone Number", value="+1 (555) 234-5678")
            b_location = st.text_input("Location", value="San Francisco, CA (or Remote)")
        with c3:
            b_linkedin = st.text_input("LinkedIn URL", value="linkedin.com/in/candidate")
            b_github = st.text_input("GitHub URL", value="github.com/candidate")

        # Section 2: Target Role & Suggested Keywords
        st.subheader("2. Target Job Role & Skills Matrix")
        b_role = st.selectbox("Target Role", available_roles, index=0)

        # Smart Keyword Suggester
        role_kw = suggest_role_keywords(b_role)
        st.write("**💡 High-Impact ATS Keywords for this Role:**")
        kw_html = "".join([f"<span class='badge-category'>{display_skill(s)}</span>" for s in (role_kw.get("core", []) + role_kw.get("secondary", []))[:10]])
        st.markdown(kw_html, unsafe_allow_html=True)

        b_skills = st.text_area("Technical & Core Skills (Comma-separated)", 
            value=", ".join([display_skill(s) for s in role_kw.get("core", [])[:5]] + ["Git", "Docker", "Problem Solving"]),
            help="List your languages, frameworks, cloud tools, and databases.")

        # Section 3: Summary with AI Generator
        st.subheader("3. Executive Professional Summary")
        col_sum_txt, col_sum_btn = st.columns([3.5, 1.2])
        with col_sum_btn:
            st.write("")
            st.write("")
            if st.button("✨ Generate AI Summary", use_container_width=True):
                with st.spinner("Synthesizing ATS summary..."):
                    generated_sum = generate_ai_summary(b_role, "3+ years software development experience", b_skills)
                    st.session_state["temp_summary"] = generated_sum
                    st.rerun()

        default_summary = st.session_state.get("temp_summary", f"Dynamic and results-driven {b_role.title()} with proven expertise in building scalable, production-grade applications. Adept at translating complex product requirements into robust, high-performance software solutions while ensuring strict code quality and modern testing standards.")
        b_summary = col_sum_txt.text_area("Professional Summary", value=default_summary, height=110)

        # Section 4: Work Experience & Bullet Rewriter
        st.subheader("4. Work Experience & Impact")
        st.caption("Format each position with Company, Role, and bullet points. Use the AI enhancer below to optimize bullet points.")
        
        b_experience = st.text_area("Work Experience Entries", 
            value=f"Software Engineer | Apex Cloud Solutions (2022 - Present)\n- Engineered distributed backend services handling over 10M daily requests with 99.9% uptime\n- Optimized database query performance, reducing p95 latency by 35%\n- Collaborated in cross-functional agile sprints to deliver critical customer features\n\nJunior Developer | Tech Innovations (2021 - 2022)\n- Developed responsive web interfaces and RESTful API endpoints\n- Automated integration testing pipelines, increasing test coverage by 40%",
            height=180
        )

        # AI Bullet Enhancer Tool
        with st.expander("🛠️ AI Bullet Point Enhancer"):
            draft_bullet = st.text_input("Draft Bullet Point", placeholder="e.g. Made an API for users to log in")
            if st.button("✨ Rewrite with Strong Action Verbs & Metrics"):
                if draft_bullet:
                    enhanced = enhance_bullet_point(draft_bullet, b_role)
                    st.info(f"**Enhanced:** • {enhanced}")

        # Section 5: Projects & Education
        st.subheader("5. Key Projects & Academic Credentials")
        col_p, col_e = st.columns(2)
        with col_p:
            b_projects = st.text_area("Projects", 
                value=f"Enterprise Scalability Suite\nBuilt a distributed telemetry pipeline using {b_skills.split(',')[0]} and Docker.\nAchieved sub-50ms data ingestion across 200 distributed nodes.\n\nAI Career Navigator\nEngineered an intelligent career readiness analyzer with real-time vector search.",
                height=150
            )
        with col_e:
            b_education = st.text_area("Education & Certifications", 
                value="Bachelor of Science in Computer Science | Accredited University (2021)\nCertifications: AWS Certified Developer, PrepNexus Career Readiness",
                height=150
            )

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🚀 Build & Optimize Complete Resume", use_container_width=True):
            with st.spinner("Compiling structured resume & calculating ATS optimization score..."):
                plain_resume, struct_resume, ats_scores = generate_resume(
                    name=b_name,
                    email=b_email,
                    phone=b_phone,
                    target_role=b_role,
                    skills=b_skills,
                    experience=b_experience,
                    projects=b_projects,
                    education=b_education,
                    location=b_location,
                    linkedin=b_linkedin,
                    github=b_github
                )
                st.session_state.resume_builder_data = struct_resume
                st.session_state.resume_builder_ats = ats_scores
                st.session_state.last_generated_plain = plain_resume

                # Save to database with real scores
                save_resume(
                    st.session_state.user_email,
                    b_role,
                    plain_resume,
                    ats_scores.get("ats_score", 80.0),
                    ats_scores.get("ats_score", 80.0)
                )

    else:  # Instant AI Auto-Generate
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("⚡ Instant One-Click AI Resume Synthesis")
        st.caption("Paste your background notes, LinkedIn text, or rough experience details and Gemini will synthesize a full structured ATS resume.")

        q_name = st.text_input("Full Name", value=st.session_state.user_name or "Candidate Name")
        q_role = st.selectbox("Target Role", available_roles, key="q_role")
        q_notes = st.text_area("Candidate Raw Background Notes / Existing Bio", 
            value="Software engineer with 2 years of experience in Python, FastAPI, React, SQL, and Docker. Built a customer dashboard, improved API performance, graduated in CS in 2022.",
            height=180
        )
        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("⚡ Synthesize Structured ATS Resume", use_container_width=True):
            with st.spinner("AI is synthesizing structured resume..."):
                plain_resume, struct_resume, ats_scores = generate_resume(
                    name=q_name,
                    email=st.session_state.user_email,
                    target_role=q_role,
                    skills=q_notes,
                    experience=q_notes,
                    projects=q_notes,
                    education="B.S. in Computer Science"
                )
                st.session_state.resume_builder_data = struct_resume
                st.session_state.resume_builder_ats = ats_scores
                st.session_state.last_generated_plain = plain_resume

                save_resume(
                    st.session_state.user_email,
                    q_role,
                    plain_resume,
                    ats_scores.get("ats_score", 82.0),
                    ats_scores.get("ats_score", 82.0)
                )

    # =====================================================
    # LIVE ATS SCORECARD & EXPORT DASHBOARD
    # =====================================================
    if st.session_state.resume_builder_ats and st.session_state.last_generated_plain:
        st.markdown("---")
        st.subheader("📈 Real-Time ATS Optimization Scorecard")

        ats = st.session_state.resume_builder_ats
        score_val = ats.get("ats_score", 85.0)

        a1, a2, a3, a4 = st.columns(4)
        with a1:
            st.metric("ATS Readiness Score", f"{score_val:.1f}%")
            st.progress(int(min(100, score_val)))
        with a2:
            st.metric("Keyword Match Rate", f"{ats.get('keyword_match_rate', 0)}%")
        with a3:
            st.metric("Section Completeness", f"{ats.get('completeness_score', 0)}%")
        with a4:
            st.metric("Action Verb Density", f"{ats.get('action_score', 0)}%")

        # Recommendations
        if ats.get("recommendations"):
            st.write("**💡 Optimization Tips:**")
            for rec in ats["recommendations"]:
                st.markdown(f"- {rec}")

        st.markdown("---")
        st.subheader("📄 Resume Preview & Multi-Template Export")

        col_tmpl, col_dl = st.columns([1, 2])
        with col_tmpl:
            template_choice = st.selectbox("Select PDF Template", [
                "🎨 Modern Clean (Indigo Accent)",
                "👔 Executive Classic (Corporate Monochrome)",
                "📑 ATS Minimalist (High-Readability)"
            ])
            tmpl_key = "modern" if "Modern" in template_choice else ("classic" if "Executive" in template_choice else "minimalist")

        # Live Text Preview
        st.text_area("Plain Text / ATS Preview", st.session_state.last_generated_plain, height=450)

        # Export Buttons
        pdf_path = generate_resume_pdf(
            st.session_state.last_generated_plain,
            output_path="generated_resumes/PrepNexus_Resume.pdf",
            template=tmpl_key
        )

        b_col1, b_col2, b_col3 = st.columns(3)
        with b_col1:
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download PDF Resume",
                    data=pdf_file,
                    file_name="PrepNexus_Resume.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        with b_col2:
            st.download_button(
                label="💾 Export as JSON Data",
                data=json.dumps(st.session_state.resume_builder_data or {}, indent=2),
                file_name="PrepNexus_Resume.json",
                mime="application/json",
                use_container_width=True
            )
        with b_col3:
            st.download_button(
                label="📄 Export ATS Plain Text",
                data=st.session_state.last_generated_plain,
                file_name="PrepNexus_Resume.txt",
                mime="text/plain",
                use_container_width=True
            )

# =====================================================
# TAB 3: AI CAREER CHATBOT
# =====================================================
def render_career_chatbot():
    st.markdown("### 🤖 PrepNexus AI Career Navigator")
    st.markdown("Get personalized advice on interview tactics, salary negotiations, ATS keyword tailoring, and technical roadmaps.")

    if "chatbot" not in st.session_state:
        st.session_state.chatbot = PrepNexusChatbot(gemini_model)
    chatbot = st.session_state.chatbot

    # Display chat history
    for chat in st.session_state.chat_history:
        if chat["role"] == "user":
            st.markdown(f"""
            <div class="chat-bubble-user">
                <strong>👤 You:</strong><br>{chat["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-bubble-bot">
                <strong>🤖 PrepNexus Assistant:</strong><br>{chat["content"]}
            </div>
            """, unsafe_allow_html=True)

    user_input = st.chat_input("Ask about interviews, resume revisions, or career strategies...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("PrepNexus AI is formulating personalized guidance..."):
            response = chatbot.get_response(user_input)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

# =====================================================
# MAIN APP ROUTER
# =====================================================
def main():
    if not st.session_state.logged_in:
        login_page()
        return

    nav = render_sidebar()

    if nav == "Admin Console" and is_admin():
        show_admin_panel()
        return

    render_header()

    tab_analyzer, tab_builder, tab_chatbot = st.tabs([
        "📊 Resume Diagnostic & ATS Gap",
        "📝 Upgraded ATS Resume Builder",
        "🤖 AI Career Navigator Chat"
    ])

    with tab_analyzer:
        render_resume_analyzer()

    with tab_builder:
        render_resume_builder()

    with tab_chatbot:
        render_career_chatbot()

    st.markdown("---")
    st.caption("PrepNexus © Enterprise AI Career Intelligence Platform | Protected by JWT & PBKDF2-SHA256")

if __name__ == "__main__":
    main()
