
import streamlit as st
import tempfile
import os
import re
import time
from PIL import Image

# =====================================================
# BACKEND IMPORTS
# =====================================================
from utils.pdf_parser import extract_text_from_pdf
from utils.text_cleaner import clean_text
from utils.skill_extractor import extract_skill
from utils.readiness_scorer import calculate_readiness

from rag.embedder import load_embeddings
from rag.retriever import retrieve_role_info
from rag.vector_store import create_vectorestore

from data.all_skills import all_skills
from data.job_roles import docs
from data.role_weights import role_skill_weights

from utils.resume_api_builder import generate_resume
from utils.pdf_exporter import generate_resume_pdf
from utils.auth import generate_otp, send_otp_email

# =====================================================
# PAGE CONFIG
# =====================================================
icon = Image.open("assets/icon.png")
logo = Image.open("assets/logo.png")

st.set_page_config(
    page_title="PrepNexus",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM PROFESSIONAL CSS
# =====================================================
st.markdown("""
<style>
.main {
    background: linear-gradient(to bottom right, #0f172a, #1e293b);
}
.block-container {
    padding-top: 2rem;
}
h1, h2, h3 {
    color: white;
}
.stButton > button {
    width: 100%;
    border-radius: 12px;
    height: 3em;
    font-weight: bold;
    background: linear-gradient(90deg, #2563eb, #1d4ed8);
    color: white;
    border: none;
}
.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
}
.metric-card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# EMAIL VALIDATION
# =====================================================
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# =====================================================
# SESSION STATE INIT
# =====================================================
def init_session():
    defaults = {
        "logged_in": False,
        "otp_sent": False,
        "generated_otp": "",
        "user_email": "",
        "otp_timestamp": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()

# =====================================================
# LOGIN PAGE
# =====================================================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image(logo, width=400)
        st.markdown("# 🔐 Welcome to PrepNexus")
        st.markdown("### AI-Powered Career Intelligence Platform")
        st.markdown("Secure OTP-based login system")

        email = st.text_input("📧 Enter Your Email Address")

        if st.button("📩 Send OTP"):
            if not email:
                st.warning("Please enter your email address")
            elif not is_valid_email(email):
                st.warning("Please enter a valid email")
            else:
                otp = generate_otp()
                success, message = send_otp_email(email, otp)

                if success:
                    st.session_state.generated_otp = otp
                    st.session_state.user_email = email
                    st.session_state.otp_sent = True
                    st.session_state.otp_timestamp = time.time()
                    st.success("✅ OTP sent successfully! Please check your inbox.")
                else:
                    st.error(f"❌ Failed to send OTP: {message}")

        # OTP Verification Section
        if st.session_state.otp_sent:
            st.markdown("---")
            user_otp = st.text_input("🔑 Enter OTP", max_chars=6)

            if st.button("✅ Verify OTP"):
                # OTP expiry: 5 minutes
                if time.time() - st.session_state.otp_timestamp > 300:
                    st.error("⏰ OTP expired. Please request a new one.")
                    st.session_state.otp_sent = False
                    st.session_state.generated_otp = ""

                elif user_otp == st.session_state.generated_otp:
                    st.session_state.logged_in = True
                    st.success("🎉 Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Invalid OTP. Please try again.")

    st.stop()

# =====================================================
# MAIN APP HEADER
# =====================================================
def app_header():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo, width=550)

    st.title("🚀 PrepNexus Interview Preparation Platform")
    st.subheader(
        "Analyze resumes, identify skill gaps, build ATS-optimized resumes, and accelerate your career growth."
    )

# =====================================================
# VECTORSTORE
# =====================================================
@st.cache_resource

def load_vectorstore():
    embeddings = load_embeddings()
    return create_vectorestore(docs, embeddings)

vectorstore = load_vectorstore()
available_roles = sorted(list(role_skill_weights.keys()))

# =====================================================
# SIDEBAR
# =====================================================
def sidebar():
    st.sidebar.image(logo, width=220)
    st.sidebar.markdown("## 🚀 PrepNexus")
    st.sidebar.markdown(f"### 👤 {st.session_state.user_email}")

    if st.sidebar.button("🚪 Logout"):
        for key in ["logged_in", "otp_sent", "generated_otp", "user_email"]:
            st.session_state[key] = False if key in ["logged_in", "otp_sent"] else ""
        st.rerun()

# =====================================================
# MAIN APP
# =====================================================
def main_app():
    app_header()
    sidebar()

    tab1, tab2 = st.tabs([
        "📊 Resume Analyzer",
        "📝 AI Resume Builder"
    ])

    # =====================================================
    # TAB 1
    # =====================================================
    with tab1:
        st.markdown("## 📄 Upload Your Resume")

        upload_file = st.file_uploader(
            "Upload PDF Resume",
            type=["pdf"]
        )

        target_role = st.selectbox(
            "🎯 Choose Target Job Role",
            available_roles
        )

        if st.button("🔍 Analyze Resume"):
            if upload_file is None:
                st.warning("Please upload your resume first.")
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(upload_file.read())
                    temp_pdf_path = tmp_file.name

                resume_text = extract_text_from_pdf(temp_pdf_path)
                cleaned_resume = clean_text(resume_text)
                resume_skills = set(extract_skill(cleaned_resume, all_skills))

                retrieved_docs = retrieve_role_info(target_role, vectorstore)
                role_text = retrieved_docs[0].page_content
                role_skills = set(extract_skill(role_text, all_skills))

                matched_skills = role_skills.intersection(resume_skills)
                missing_skills = role_skills - resume_skills

                basic_match_score = (
                    (len(matched_skills) / len(role_skills)) * 100
                    if role_skills else 0
                )

                weighted_result = calculate_readiness(
                    resume_skills,
                    role_skill_weights[target_role]
                )

                readiness_score = weighted_result["readiness_score"]

                st.success("✅ Resume Analysis Complete")

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("ATS Match Score", f"{basic_match_score:.2f}%")
                with col2:
                    st.metric("Career Readiness", f"{readiness_score:.2f}%")

                st.subheader("📊 Performance Dashboard")
                st.write("ATS Match score")
                st.progress(int(basic_match_score))

                st.write("Career Readiness Score")
                st.progress(
                    int(readiness_score)
                )

                st.subheader("📌 Missing Skills")
                st.write(sorted(missing_skills))

                st.subheader("✅ Matched Skills")
                st.write(sorted(matched_skills))

                           # =====================================================
# CAREER PREFERENCE
# =====================================================

                st.markdown("---")
                st.subheader("🎯 Career Preference")
                st.write(target_role)


# =====================================================
# ROLE DESCRIPTION
# =====================================================

                st.subheader("📘 Role Description")
                st.write(role_text)


# =====================================================
# REQUIRED SKILLS
# =====================================================

                st.subheader("📌 Required Skills")
                st.write(sorted(role_skills))


# =====================================================
# CORE / SECONDARY / ADVANCED BREAKDOWN
# =====================================================

                st.markdown("---")
                st.subheader("🚀 Advanced Skill Breakdown")

                col_core, col_secondary, col_advanced = st.columns(3)

                with col_core:
                  st.markdown("### 🧠 Core Skills")
                  st.write("Matched:", sorted(weighted_result["core_matched"]))
                  st.write("Missing:", sorted(weighted_result["missing_core"]))

                with col_secondary:
                  st.markdown("### ⚙️ Secondary Skills")
                  st.write("Matched:", sorted(weighted_result["secondary_matched"]))
                  st.write("Missing:", sorted(weighted_result["missing_secondary"]))

                with col_advanced:
                  st.markdown("### 🔬 Advanced Skills")
                  st.write("Matched:", sorted(weighted_result["advanced_matched"]))
                  st.write("Missing:", sorted(weighted_result["missing_advanced"]))


# =====================================================
# STATUS
# =====================================================

                st.markdown("---")
                st.subheader("📈 Candidate Status")

                if readiness_score >= 85:
                   st.success("Highly Job Ready")

                elif readiness_score >= 70:
                   st.info("Job Ready")

                elif readiness_score >= 50:
                  st.warning("Moderate Readiness")

                else:
                 st.error("Significant Skill Gap")


# =====================================================
# RECOMMENDATION
# =====================================================

                st.subheader("💡 Career Recommendation")

                if readiness_score >= 85:
                  st.success(
                     "You are highly competitive. Focus on portfolio, projects, and interviews."
                     )
   
                elif readiness_score >= 70:
                 st.info(
                    "You are job-ready. Strengthen secondary and advanced skills."
                     )

                elif readiness_score >= 50:
                  st.warning(
                    "Focus on missing core skills first."
                    )

                else:
                  st.error(
                     "Prioritize foundational skill development before applying aggressively."
                      )

                os.remove(temp_pdf_path)

    # =====================================================
    # TAB 2
    # =====================================================
    with tab2:
        st.markdown("## 📝 Build Your ATS Resume")

        name = st.text_input("Full Name")
        email = st.text_input("Email", value=st.session_state.user_email)
        phone = st.text_input("Phone Number")
        role = st.selectbox("Target Role", available_roles)

        skills = st.text_area("Skills")
        experience = st.text_area("Experience")
        projects = st.text_area("Projects")
        education = st.text_area("Education")

        if st.button("🚀 Generate Resume"):
            generated_resume = generate_resume(
                name=name,
                email=email,
                phone=phone,
                target_role=role,
                skills=skills,
                experience=experience,
                projects=projects,
                education=education
            )

            st.success("✅ Resume Generated Successfully")
            st.text_area("Resume Preview", generated_resume, height=600)

            pdf_path = generate_resume_pdf(generated_resume)

            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download Resume PDF",
                    data=pdf_file,
                    file_name="PrepNexus_Resume.pdf",
                    mime="application/pdf"
                )

# =====================================================
# ROUTER
# =====================================================
if not st.session_state.logged_in:
    login_page()
else:
    main_app()

# =====================================================
# FOOTER
# =====================================================
st.markdown("---")
st.caption("PrepNexus © AI-Powered Career Intelligence Platform")
