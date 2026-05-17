
import streamlit as st
import tempfile
import os
import re
import time
from PIL import Image
import importlib


def _import_faiss():
    """Dynamically import FAISS from the available langchain package.
    Tries `langchain_community.vectorstores` first, then `langchain.vectorstores`.
    """
    for mod_name in ("langchain_community.vectorstores", "langchain.vectorstores"):
        try:
            mod = importlib.import_module(mod_name)
            return getattr(mod, "FAISS")
        except Exception:
            continue
    raise ImportError("Could not import FAISS from langchain packages. Install langchain-community or langchain.")


FAISS = _import_faiss()

# =====================================================
# BACKEND IMPORTS
# =====================================================
from utils.pdf_parser import extract_text_from_pdf
from utils.text_cleaner import clean_text
from utils.skill_extractor import extract_skill,normalize_skill
from utils.readiness_scorer import calculate_readiness

from rag.embedder import load_embeddings

from rag.vector_store import create_vectorestore

from data.all_skills import all_skills
from data.job_roles import docs
from data.role_weights import role_skill_weights


from utils.pdf_exporter import generate_resume_pdf
from utils.auth import hash_password

from database.crud import (
    get_user_by_email,
    register_user,
    authenticate_user,
    save_resume,
    get_user_resumes
)
from database.init_db import initialize_database

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
            .skill-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(90deg, #0f172a, #0b2c66);
    padding: 18px 24px;
    border-radius: 16px;
    margin-bottom: 12px;
    border-left: 4px solid #3b82f6;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
}

.skill-name {
    color: #ffffff;
    font-size: 22px;
    font-weight: 600;
    letter-spacing: 0.3px;
}

.skill-score {
    background-color: #2563eb;
    color: white;
    padding: 6px 16px;
    border-radius: 12px;
    font-size: 16px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# EMAIL VALIDATION
# =====================================================
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_password(password):
    if len(password) < 8:
        return False
    return bool(
        re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"\d", password)
    )

# =====================================================
# SESSION STATE INIT
# =====================================================
def init_session():
    defaults = {
        "logged_in": False,
        "user_email": "",
        "user_name": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session()
initialize_database()

# =====================================================
# LOGIN PAGE
# =====================================================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image(
            logo,
            width=400
        )

        st.markdown(
            "# 🔐 Welcome to PrepNexus"
        )

        st.markdown(
            "### AI-Powered Career Intelligence Platform"
        )

        st.markdown(
            "Secure password-based authentication system"
        )

        # =====================================================
        # LOGIN OR CREATE ACCOUNT MODE
        # =====================================================

        auth_mode = st.radio(
            "Select Mode",
            [
                "Login",
                "Create Account"
            ]
        )

        # =====================================================
        # NAME FIELD FOR CREATE ACCOUNT
        # =====================================================

        name = ""

        if auth_mode == "Create Account":
            name = st.text_input(
                "👤 Enter Your Full Name"
            )

        # =====================================================
        # EMAIL FIELD
        # =====================================================

        email = st.text_input(
            "📧 Enter Your Email Address"
        )

        # =====================================================
        # AUTHENTICATION ACTION
        # =====================================================

        password = st.text_input(
            "🔐 Password",
            type="password"
        )

        confirm_password = ""
        if auth_mode == "Create Account":
            confirm_password = st.text_input(
                "🔐 Confirm Password",
                type="password"
            )

        st.markdown("---")
        st.caption("Password must be at least 8 characters and include uppercase, lowercase, and digits.")

        if st.button("✅ Continue"):
            normalized_email = email.strip().lower()

            if not email:
                st.warning("Please enter your email address.")
            elif not is_valid_email(email):
                st.warning("Please enter a valid email address.")
            elif auth_mode == "Create Account" and not name:
                st.warning("Please enter your full name.")
            elif not password:
                st.warning("Please enter your password.")
            elif auth_mode == "Create Account" and password != confirm_password:
                st.warning("Passwords do not match. Please confirm your password.")
            elif auth_mode == "Create Account" and not is_valid_password(password):
                st.warning("Choose a stronger password with uppercase, lowercase, and digits.")
            else:
                existing_user = get_user_by_email(normalized_email)

                if auth_mode == "Create Account":
                    if existing_user:
                        st.warning("⚠️ Account already exists. Please login instead.")
                    else:
                        password_hash = hash_password(password)
                        user = register_user(name, normalized_email, password_hash)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user_email = normalized_email
                            st.session_state.user_name = name
                            st.success("✅ Account created and logged in successfully.")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Failed to create account. Please try again.")

                elif auth_mode == "Login":
                    if not existing_user:
                        st.warning("⚠️ Account not found. Please create an account first.")
                    else:
                        if not existing_user.password_hash and existing_user.otp:
                            st.warning(
                                "This account was created with legacy OTP login. "
                                "Enter the OTP sent to your email as a temporary password to migrate your account."
                            )

                        user = authenticate_user(normalized_email, password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user_email = normalized_email
                            st.session_state.user_name = user.name or ""
                            st.success("🎉 Login successful!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials. Please try again.")

    st.stop()

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
    index_dir = os.path.join(os.path.dirname(__file__), "rag", "job_index")
    index_faiss = os.path.join(index_dir, "index.faiss")
    index_pkl = os.path.join(index_dir, "index.pkl")

    if os.path.exists(index_dir) and os.path.exists(index_faiss) and os.path.exists(index_pkl):
        try:
            vectorestore = FAISS.load_local(
                index_dir,
                embeddings,
                allow_dangerous_deserialization=True
            )
            return vectorestore
        except Exception as exc:
            st.warning(
                "Could not load FAISS index locally; falling back to internal role profiles."
            )
            st.exception(exc)

    if not os.path.exists(index_dir):
        st.warning(
            f"FAISS index directory not found: {index_dir}. Using fallback role matching instead."
        )
    else:
        missing_files = []
        if not os.path.exists(index_faiss):
            missing_files.append("index.faiss")
        if not os.path.exists(index_pkl):
            missing_files.append("index.pkl")
        if missing_files:
            st.warning(
                f"FAISS index files missing: {', '.join(missing_files)}. Using fallback role matching instead."
            )

    return None


def get_role_profile_text(role):
    role_data = role_skill_weights.get(role)
    if not role_data:
        return f"{role.title()} role description is not available."

    core = ", ".join(role_data.get("core", []))
    secondary = ", ".join(role_data.get("secondary", []))
    advanced = ", ".join(role_data.get("advanced", []))

    description_parts = []
    if core:
        description_parts.append(f"Core skills: {core}")
    if secondary:
        description_parts.append(f"Secondary skills: {secondary}")
    if advanced:
        description_parts.append(f"Advanced skills: {advanced}")

    return f"{role.title()} requires {core}. " + " ".join(description_parts)


available_roles = sorted(list(role_skill_weights.keys()))

# =====================================================
# SIDEBAR
# =====================================================
def sidebar():
    st.sidebar.image(logo, width=220)
    st.sidebar.markdown("## 🚀 PrepNexus")
    st.sidebar.markdown(f"### 👤 {st.session_state.user_name or st.session_state.user_email}")

    if st.sidebar.button("🚪 Logout"):
        for key in ["logged_in", "user_email", "user_name"]:
            st.session_state[key] = False if key == "logged_in" else ""
        st.rerun()

# =====================================================
# MAIN APP
# =====================================================
def render_skill_category(title, matched, missing, color):
    total = len(matched) + len(missing)
    progress = int((len(matched) / total) * 100) if total > 0 else 0

    # --------------------
    st.markdown(f"""
    <div style="
        background:#ffffff;
        padding:25px;
        border-radius:18px;
        border-top:5px solid {color};
        box-shadow:0 8px 24px rgba(0,0,0,0.15);
        margin-bottom:15px;
    ">
        <h2 style="
            color:#1e293b;
            font-size:30px;
            font-weight:800;
            margin:0;
        ">
            {title}
        </h2>
    </div>
    """, unsafe_allow_html=True)

    # Progress
    st.metric("Completion", f"{progress}%")
    st.caption(f"{len(matched)} of {total} skills matched")
    st.progress(progress)

    # Matched Skills
    st.markdown("### ✅ Matched Skills")
    if matched:
        for skill in sorted(matched):
            st.markdown(
                f"""
                <div style="
                    background:#dcfce7;
                    padding:10px;
                    border-radius:8px;
                    margin-bottom:6px;
                    color:#166534;
                    font-weight:600;
                ">
                    ✔️ {display_skill(skill)}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("No matched skills yet.")

    # Missing Skills
    st.markdown("### ❌ Missing Skills")
    if missing:
        for skill in sorted(missing):
            st.markdown(
                f"""
                <div style="
                    background:#fee2e2;
                    padding:10px;
                    border-radius:8px;
                    margin-bottom:6px;
                    color:#991b1b;
                    font-weight:600;
                ">
                    ❌ {display_skill(skill)}
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.success("All skills covered!")

def display_skill(skill):
    """
    Convert normalized backend skill names into polished,
    recruiter-friendly production UI labels.
    """

    skill = skill.strip().lower()

    display_map = {
        # =====================================================
        # DATA SCIENCE / MACHINE LEARNING
        # =====================================================
        "scikit learn": "Scikit-Learn",
        "machine learning": "Machine Learning",
        "deep learning": "Deep Learning",
        "data science": "Data Science",
        "data analysis": "Data Analysis",
        "data visualization": "Data Visualization",
        "statistics": "Statistics",
        "power bi": "Power BI",
        "tableau": "Tableau",
        "excel": "Excel",
        "sql": "SQL",
        "mysql": "MySQL",
        "postgresql": "PostgreSQL",
        "mongodb": "MongoDB",

        # Libraries / Frameworks
        "numpy": "NumPy",
        "pandas": "Pandas",
        "matplotlib": "Matplotlib",
        "seaborn": "Seaborn",
        "tensorflow": "TensorFlow",
        "pytorch": "PyTorch",
        "keras": "Keras",
        "opencv": "OpenCV",
        "xgboost": "XGBoost",
        "lightgbm": "LightGBM",

        # =====================================================
        # PROGRAMMING LANGUAGES
        # =====================================================
        "python": "Python",
        "java": "Java",
        "javascript": "JavaScript",
        "typescript": "TypeScript",
        "c": "C",
        "c++": "C++",
        "c#": "C#",
        "r": "R",
        "go": "Go",
        "php": "PHP",
        "swift": "Swift",
        "kotlin": "Kotlin",

        # =====================================================
        # WEB DEVELOPMENT
        # =====================================================
        "html": "HTML",
        "css": "CSS",
        "react": "React",
        "react.js": "React.js",
        "reactjs": "React.js",
        "next.js": "Next.js",
        "nextjs": "Next.js",
        "node.js": "Node.js",
        "nodejs": "Node.js",
        "express.js": "Express.js",
        "expressjs": "Express.js",
        "fastapi": "FastAPI",
        "flask": "Flask",
        "django": "Django",
        "streamlit": "Streamlit",
        "bootstrap": "Bootstrap",
        "tailwind css": "Tailwind CSS",

        # =====================================================
        # CLOUD / DEVOPS
        # =====================================================
        "amazon web services": "AWS",
        "aws": "AWS",
        "google cloud platform": "GCP",
        "gcp": "GCP",
        "microsoft azure": "Azure",
        "azure": "Azure",
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "jenkins": "Jenkins",
        "terraform": "Terraform",
        "git": "Git",
        "github": "GitHub",
        "gitlab": "GitLab",
        "ci cd": "CI/CD",
        "ci/cd": "CI/CD",
        "mlops": "MLOps",
        "llms": "LLMs",
        "fine tuning": "Fine-tuning",
        "openai api": "OpenAI API",
        "large language models": "Large Language Models",
        "prompt engineering": "Prompt Engineering",
        "retrieval augmented generation": "RAG",

        # =====================================================
        # SECURITY / AUTH
        # =====================================================
        "jwt": "JWT",
        "oauth": "OAuth",
        "rest api": "REST API",
        "graphql": "GraphQL",

        # =====================================================
        # BUSINESS / PRODUCTIVITY
        # =====================================================
        "project management": "Project Management",
        "business analysis": "Business Analysis",
        "product management": "Product Management",

        # =====================================================
        # GENERIC
        # =====================================================
        "ai": "AI",
        "nlp": "NLP",
        "computer vision": "Computer Vision",
        "llm": "LLM",
        "rag": "RAG",
    }

    # Return mapped professional label
    if skill in display_map:
        return display_map[skill]

    # Default fallback formatting
    return " ".join(word.capitalize() for word in skill.split())





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

                from rag.retriever import retrieve_role_info

                temp_pdf_path = None
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(upload_file.read())
                    temp_pdf_path = tmp_file.name

                try:
                    with st.spinner("Loading AI analysis engine..."):
                        vectorstore = load_vectorstore()

                    resume_text = extract_text_from_pdf(temp_pdf_path)
                    cleaned_resume = clean_text(resume_text)
                    resume_skills = set(normalize_skill(skill)
                                        for skill in extract_skill(cleaned_resume, all_skills))

                    if vectorstore is not None:
                        retrieved_docs = retrieve_role_info(target_role, vectorstore)
                        if retrieved_docs:
                            role_text = retrieved_docs[0].page_content
                        else:
                            role_text = get_role_profile_text(target_role)
                            st.warning(
                                "Could not retrieve a role document from the vector database. "
                                "Using internal role profile fallback."
                            )
                    else:
                        role_text = get_role_profile_text(target_role)
                        st.info(
                            "Using internal role profile fallback for resume analysis."
                        )

                    extracted_role_skills = set(
                        normalize_skill(skill)
                        for skill in extract_skill(role_text, all_skills)
                    )

                    expected_role_skills = set(
                        normalize_skill(skill)
                        for section in role_skill_weights[target_role].values()
                        for skill in section
                    )

                    use_expected_role_skills = not extracted_role_skills
                    if use_expected_role_skills:
                        st.warning(
                            "No skills could be extracted from the role text. "
                            "Showing the expected role skills for the selected position."
                        )

                    role_skills = extracted_role_skills.union(expected_role_skills)
                    matched_skills = expected_role_skills.intersection(resume_skills)
                    missing_skills = expected_role_skills - resume_skills

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

                    if missing_skills:
                        for skill in sorted(missing_skills):
                            st.markdown(
                                f"<div style='background:#fee2e2; padding:10px; border-radius:8px; margin-bottom:6px; color:black;'>❌ {display_skill(skill)}</div>",
                                unsafe_allow_html=True
                            )
                    else:
                        st.success("No major skill gaps detected.")

                    st.subheader("✅ Matched Skills")

                    if matched_skills:
                        for skill in sorted(matched_skills):
                            st.markdown(
                                f"<div style='background:#dcfce7; padding:10px; border-radius:8px; margin-bottom:6px; color:black;'>✔️ {display_skill(skill)}</div>",
                                unsafe_allow_html=True
                            )
                    else:
                        st.warning("No matched skills detected.")

                    # CAREER PREFERENCE
                    st.markdown("---")
                    st.subheader("🎯 Career Preference")
                    st.write(target_role)

                    # ROLE DESCRIPTION
                    st.subheader("📘 Role Description")
                    st.markdown(f"""
                    <div style="
                        background:#f8fafc;
                        padding:25px;
                        border-radius:18px;
                        border-left:6px solid #2563eb;
                        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
                        margin-bottom:20px;
                        ">
                        <h3 style="
                            color:#1e293b;
                            font-weight:700;
                            margin-bottom:15px;
                        ">
                            🎯 {target_role.title()} Career Overview
                        </h3>
                    </div>
                    """, unsafe_allow_html=True)
                    st.info(role_text)

                    st.subheader("📌 Required Skills")
                    if use_expected_role_skills:
                        st.info(
                            "Using role expectations from the internal position profile because the job description text did not yield extractable skills."
                        )

                    for skill in sorted(role_skills):
                       st.markdown(
                           f"""
                           <div class="skill-card">
                               <div class="skill-name">🎯 {display_skill(skill)}</div>
                          </div>
                        """,
                       unsafe_allow_html=True
    )

                    st.markdown("---")
                    st.subheader("🚀 Advanced Skill Intelligence Dashboard")

                    col_core, col_secondary, col_advanced = st.columns(3)
                    with col_core:
                        render_skill_category(
                            "🧠 Core Skills",
                            weighted_result["core_matched"],
                            weighted_result["missing_core"],
                            "#ef4444"
                        )

                    with col_secondary:
                        render_skill_category(
                            "⚙️ Secondary Skills",
                            weighted_result["secondary_matched"],
                            weighted_result["missing_secondary"],
                            "#8b5cf6"
                        )

                    with col_advanced:
                        render_skill_category(
                            "🔬 Advanced Skills",
                            weighted_result["advanced_matched"],
                            weighted_result["missing_advanced"],
                            "#10b981"
                        )

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

                except Exception as e:
                    st.error(
                        "Resume analysis failed. Please try again or contact support."
                    )
                    st.exception(e)

                finally:
                    if temp_pdf_path and os.path.exists(temp_pdf_path):
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
            from utils.resume_api_builder import generate_resume
            try:
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

            except Exception as e:
                st.error("Resume generation failed. Please check your input and try again.")
                st.exception(e)

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
