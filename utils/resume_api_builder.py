import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=env_path, override=True)


@st.cache_resource
def get_gemini_model():
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise EnvironmentError(
            f"GEMINI_API_KEY is not set. Checked path: {env_path}"
        )

    genai.configure(api_key=api_key)

    # Faster fixed model
    MODEL_NAME = "gemini-1.5-flash"

    model = genai.GenerativeModel(MODEL_NAME)

    return model


def generate_resume(
    name,
    email,
    phone,
    target_role,
    skills,
    experience,
    projects,
    education
):
    model = get_gemini_model()

    prompt = f"""
Create a professional ATS-optimized resume for the following candidate.

Candidate Details:
Name: {name}
Email: {email}
Phone: {phone}
Target Role: {target_role}

Education:
{education}

Skills:
{skills}

Experience:
{experience}

Projects:
{projects}

OUTPUT FORMAT:

{name.upper()}
Email: {email} | Phone: {phone}
Target Role: {target_role}

Professional Summary:
Write 3-4 strong lines based on the candidate details.

Technical Skills:
- Programming Languages
- Web/Frameworks
- Database
- Tools/Platforms
- Other Skills

Education:
Rewrite education professionally.

Projects:
For each project:
Project Name
- What the project does
- Tech stacks
- Impact or outcome

Experience:
If experience is available, rewrite professionally.
If fresher, write:
"Fresher with hands-on academic and project experience."

Certifications:
Write "Available upon request" if not provided.

Strengths:
- Problem solving
- Quick learning
- Team collaboration
- Communication

ATS Keywords:
Add relevant keywords for {target_role}.
"""

    response = model.generate_content(prompt)

    return response.text