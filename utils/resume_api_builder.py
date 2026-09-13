import os
import streamlit as st
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=env_path, override=True)

from utils.gemini_config import get_configured_gemini_model
from utils.structured_output import (
    call_gemini_structured,
    ResumeDataSchema,
    format_structured_resume_plain_text,
    calculate_resume_ats_score,
)
from data.role_weights import role_skill_weights


@st.cache_resource
def get_gemini_model():
    """
    Cached accessor for Gemini generative model with fallback support.
    """
    model = get_configured_gemini_model()
    if model is None:
        raise EnvironmentError(f"GEMINI_API_KEY is not configured in {env_path}")
    return model


def build_local_structured_resume(
    name: str,
    email: str,
    phone: str = "",
    target_role: str = "",
    skills: str = "",
    experience: str = "",
    projects: str = "",
    education: str = "",
    location: str = "",
    linkedin: str = "",
    github: str = "",
    portfolio: str = "",
) -> dict:
    """
    Build a comprehensive fallback structured resume dictionary locally without API dependency.
    """
    # Parse skills
    clean_skills = [s.strip() for s in skills.replace("\n", ",").split(",") if s.strip()]
    langs = [s for s in clean_skills if s.lower() in {"python", "javascript", "typescript", "java", "c++", "c#", "go", "sql", "html", "css", "r"}]
    frameworks = [s for s in clean_skills if s.lower() in {"react", "react.js", "next.js", "node.js", "express.js", "django", "flask", "fastapi", "vue.js", "angular", "tailwind css", "bootstrap"}]
    db_cloud = [s for s in clean_skills if s.lower() in {"aws", "gcp", "azure", "docker", "kubernetes", "postgresql", "mysql", "mongodb", "redis", "sqlite"}]
    tools = [s for s in clean_skills if s not in langs and s not in frameworks and s not in db_cloud]

    if not langs and clean_skills:
        langs = clean_skills[:3]
    if not frameworks and len(clean_skills) > 3:
        frameworks = clean_skills[3:6]
    if not tools and len(clean_skills) > 6:
        tools = clean_skills[6:]

    # Parse projects
    project_items = []
    if projects:
        raw_projs = [p.strip() for p in projects.split("\n\n") if p.strip()]
        for p in raw_projs:
            lines = [line.strip() for line in p.split("\n") if line.strip()]
            p_name = lines[0].lstrip("-• ") if lines else "Featured Engineering Project"
            p_desc = lines[1] if len(lines) > 1 else f"Designed and deployed a scalable solution using modern technologies."
            project_items.append({
                "name": p_name,
                "description": p_desc,
                "tech_stack": clean_skills[:4] if clean_skills else ["Python", "Git"],
                "key_achievements": [
                    f"Engineered end-to-end functionality resulting in improved workflow efficiency.",
                    f"Implemented robust automated test coverage and documentation."
                ],
                "live_url": "",
                "github_url": github or ""
            })
    else:
        project_items.append({
            "name": f"{target_role.title()} Portfolio Application",
            "description": f"Full-stack production project demonstrating proficiency in {target_role.title()} requirements.",
            "tech_stack": clean_skills[:4] or ["Python", "FastAPI"],
            "key_achievements": [
                "Built responsive UI and scalable backend endpoints with error handling.",
                "Optimized application latency and adhered to modern engineering best practices."
            ],
            "live_url": "",
            "github_url": github or ""
        })

    # Parse experience
    exp_items = []
    if experience:
        raw_exps = [e.strip() for e in experience.split("\n\n") if e.strip()]
        for e in raw_exps:
            e_lines = [line.strip() for line in e.split("\n") if line.strip()]
            exp_items.append({
                "role": e_lines[0].lstrip("-• ") if e_lines else f"{target_role.title()} Specialist",
                "company_or_academic": e_lines[1] if len(e_lines) > 1 else "Tech Innovations Inc.",
                "duration": "2023 - Present",
                "location": location or "Remote",
                "key_responsibilities": [
                    f"Collaborated with cross-functional teams to implement scalable {target_role} features.",
                    "Improved performance metrics and reduced operational overhead by 25%.",
                    "Maintained code quality through automated reviews and unit tests."
                ]
            })
    else:
        exp_items.append({
            "role": f"{target_role.title()} Developer / Intern",
            "company_or_academic": "Academic & Open-Source Projects",
            "duration": "2023 - Present",
            "location": location or "Remote",
            "key_responsibilities": [
                f"Designed and delivered functional modules aligned with {target_role} benchmarks.",
                "Participated in agile code sprints, debugging, and continuous improvement cycles."
            ]
        })

    # Summary
    summary = (
        f"Dynamic and results-driven {target_role.title()} professional with a strong foundation in "
        f"{', '.join(clean_skills[:4]) if clean_skills else 'software engineering'}. "
        f"Proven ability to translate technical specifications into robust, maintainable solutions with high attention to performance and code quality."
    )

    return {
        "name": name.strip(),
        "email": email.strip(),
        "phone": phone.strip(),
        "location": location.strip(),
        "linkedin": linkedin.strip(),
        "github": github.strip(),
        "portfolio": portfolio.strip(),
        "target_role": target_role.strip(),
        "seniority_level": "Mid-Level",
        "professional_summary": summary,
        "technical_skills": {
            "programming_languages": langs or ["Python", "SQL"],
            "frameworks_and_libraries": frameworks or ["FastAPI", "React"],
            "databases_and_cloud": db_cloud or ["PostgreSQL", "Docker"],
            "tools_and_platforms": tools or ["Git", "GitHub Actions", "Linux"],
            "soft_skills": ["Problem Solving", "Team Collaboration", "Agile Execution"]
        },
        "education": education.strip() or "Bachelor of Science in Computer Science / Engineering",
        "education_items": [
            {
                "degree": education.strip() or "B.S. in Computer Science",
                "institution": "Accredited University",
                "year": "2024",
                "details": "Coursework: Data Structures, Algorithms, Systems Architecture"
            }
        ],
        "projects": project_items,
        "experience": exp_items,
        "certifications": ["AWS Certified Cloud Practitioner (or equivalent)", "PrepNexus Certified Readiness"],
        "strengths": ["Rapid Prototyping", "Clean Architecture", "Critical Thinking"],
        "ats_keywords": [target_role, "Agile", "Full Life Cycle", "REST APIs", "CI/CD"]
    }


def generate_ai_summary(target_role: str, experience_summary: str, skills: str) -> str:
    """
    Generate a tailored, 3-sentence high-impact ATS summary using Gemini.
    """
    prompt = f"""
    Write an impactful 3-sentence professional summary for an ATS resume.
    Role: {target_role}
    Experience/Background: {experience_summary}
    Key Skills: {skills}

    Requirements:
    - Include high-impact ATS keywords relevant to {target_role}.
    - Highlight problem solving, technical execution, and business value.
    - Do not use first-person pronouns (I, me, my).
    - Return ONLY the summary paragraph.
    """
    try:
        model = get_gemini_model()
        resp = model.generate_content(prompt)
        text = getattr(resp, "text", "").strip()
        if text:
            return text
    except Exception:
        pass

    return (
        f"Results-oriented {target_role.title()} professional equipped with hands-on expertise in {skills or 'software engineering'}. "
        f"Demonstrated track record of delivering resilient, production-ready software solutions with focus on scalability and performance. "
        f"Passionate about leveraging modern development methodologies to drive measurable organizational impact."
    )


def enhance_bullet_point(draft_bullet: str, target_role: str) -> str:
    """
    Rewrite a draft work experience bullet point into a high-impact, quantified achievement bullet.
    """
    if not draft_bullet or not draft_bullet.strip():
        return draft_bullet

    prompt = f"""
    Rewrite the following resume bullet point to make it compelling, action-oriented, and ATS-optimized for a {target_role} position.
    Draft: "{draft_bullet}"
    
    Guidelines:
    - Start with a strong action verb (e.g., Architected, Spearheaded, Engineered, Streamlined).
    - Include a realistic quantified metric or business impact (e.g., improved efficiency by 30%, reduced latency by 40ms).
    - Keep it under 25 words.
    - Return ONLY the rewritten bullet point without quotation marks.
    """
    try:
        model = get_gemini_model()
        resp = model.generate_content(prompt)
        text = getattr(resp, "text", "").strip().lstrip("•-* ")
        if text:
            return text
    except Exception:
        pass

    return f"Engineered and deployed robust {target_role} capabilities, optimizing execution efficiency by 35% across core modules."


def suggest_role_keywords(target_role: str) -> dict:
    """
    Returns curated core, secondary, and advanced skills for a given job role.
    """
    role_key = target_role.strip().lower()
    return role_skill_weights.get(role_key, {
        "core": ["problem solving", "git", "communication"],
        "secondary": ["unit testing", "code review"],
        "advanced": ["system design", "performance tuning"]
    })


def generate_resume(
    name: str,
    email: str,
    phone: str = "",
    target_role: str = "Software Developer",
    skills: str = "",
    experience: str = "",
    projects: str = "",
    education: str = "",
    location: str = "",
    linkedin: str = "",
    github: str = "",
    portfolio: str = "",
) -> tuple[str, dict, dict]:
    """
    Generate an ATS-optimized structured resume.
    Returns: (plain_text_resume, structured_dict, ats_scoring_metrics)
    """
    prompt = f"""
    Return a single valid JSON object representing an ATS-optimized professional resume.
    You MUST output top-level keys exactly matching this structure:
    {{
      "name": "{name}",
      "email": "{email}",
      "phone": "{phone}",
      "location": "{location}",
      "linkedin": "{linkedin}",
      "github": "{github}",
      "portfolio": "{portfolio}",
      "target_role": "{target_role}",
      "seniority_level": "Mid-Level",
      "professional_summary": "High-impact 3-sentence summary with ATS keywords...",
      "technical_skills": {{
        "programming_languages": ["Language 1", "Language 2"],
        "frameworks_and_libraries": ["Framework 1"],
        "databases_and_cloud": ["Cloud/DB 1"],
        "tools_and_platforms": ["Tool 1"],
        "soft_skills": ["Problem Solving", "Team Collaboration"]
      }},
      "education": "{education or 'B.S. in Computer Science'}",
      "education_items": [
        {{
          "degree": "{education or 'B.S. in Computer Science'}",
          "institution": "University / College",
          "year": "2024",
          "details": "Relevant Coursework & Achievements"
        }}
      ],
      "projects": [
        {{
          "name": "Project Name",
          "description": "Short project summary",
          "tech_stack": ["Tech1", "Tech2"],
          "key_achievements": ["Quantified result or impact metric"],
          "live_url": "",
          "github_url": "{github}"
        }}
      ],
      "experience": [
        {{
          "role": "Role Title",
          "company_or_academic": "Organization Name",
          "duration": "2023 - Present",
          "location": "{location or 'Remote'}",
          "key_responsibilities": [
            "Action verb achievement bullet with metrics",
            "Performance optimization achievement"
          ]
        }}
      ],
      "certifications": ["Relevant Certification"],
      "strengths": ["Analytical Thinking", "Fast Learner"],
      "ats_keywords": ["{target_role}", "Scalability", "Clean Code", "CI/CD"]
    }}

    Candidate Provided Data:
    - Name: {name}
    - Email: {email}
    - Phone: {phone}
    - Target Role: {target_role}
    - Skills: {skills}
    - Background/Experience: {experience}
    - Projects: {projects}
    - Education: {education}
    """

    structured_data = None
    try:
        model = get_gemini_model()
        structured_data = call_gemini_structured(model, prompt, schema_class=ResumeDataSchema)
    except Exception as exc:
        print(f"Gemini structured resume error: {exc}")

    if not structured_data or not isinstance(structured_data, dict) or not structured_data.get("professional_summary"):
        structured_data = build_local_structured_resume(
            name=name,
            email=email,
            phone=phone,
            target_role=target_role,
            skills=skills,
            experience=experience,
            projects=projects,
            education=education,
            location=location,
            linkedin=linkedin,
            github=github,
            portfolio=portfolio
        )

    # Format text and calculate ATS metrics
    plain_text = format_structured_resume_plain_text(structured_data)
    ats_metrics = calculate_resume_ats_score(structured_data, target_role)

    return plain_text, structured_data, ats_metrics