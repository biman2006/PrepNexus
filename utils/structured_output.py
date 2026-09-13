import json
import re
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# =====================================================
# PYDANTIC SCHEMAS FOR STRUCTURED AI OUTPUT
# =====================================================

class ContactInfoSchema(BaseModel):
    name: str = Field(..., description="Full Name")
    email: str = Field(..., description="Email Address")
    phone: str = Field(default="", description="Phone Number")
    location: str = Field(default="", description="City, Country or Remote")
    linkedin: str = Field(default="", description="LinkedIn profile URL")
    github: str = Field(default="", description="GitHub profile URL")
    portfolio: str = Field(default="", description="Personal portfolio or website URL")


class TechnicalSkillsSchema(BaseModel):
    programming_languages: List[str] = Field(default_factory=list, description="List of programming languages")
    frameworks_and_libraries: List[str] = Field(default_factory=list, description="List of web/ML frameworks & libraries")
    databases_and_cloud: List[str] = Field(default_factory=list, description="Databases, SQL, NoSQL, and Cloud platforms")
    tools_and_platforms: List[str] = Field(default_factory=list, description="Developer tools, CI/CD, Git, DevOps")
    soft_skills: List[str] = Field(default_factory=lambda: ["Problem Solving", "Team Collaboration", "Agile Communication"])


class ProjectItemSchema(BaseModel):
    name: str = Field(..., description="Project name")
    description: str = Field(default="", description="Short summary of project objectives")
    tech_stack: List[str] = Field(default_factory=list, description="Technologies used")
    key_achievements: List[str] = Field(default_factory=list, description="Quantified impact or results achieved")
    live_url: str = Field(default="", description="Live application or demo link")
    github_url: str = Field(default="", description="Source code repository link")


class ExperienceItemSchema(BaseModel):
    role: str = Field(..., description="Job or internship role title")
    company_or_academic: str = Field(..., description="Company, organization, or academic laboratory")
    duration: str = Field(default="Present", description="Timeline or duration (e.g. Jun 2023 - Present)")
    location: str = Field(default="", description="Location or Remote")
    key_responsibilities: List[str] = Field(default_factory=list, description="Bullet points with action verbs and metrics")


class EducationItemSchema(BaseModel):
    degree: str = Field(..., description="Degree title (e.g. B.Tech in Computer Science)")
    institution: str = Field(..., description="University or college name")
    year: str = Field(default="", description="Graduation year or range")
    details: str = Field(default="", description="GPA, coursework, or academic honors")


class ResumeDataSchema(BaseModel):
    name: str = Field(..., description="Candidate full name")
    email: str = Field(..., description="Candidate email")
    phone: str = Field(default="", description="Candidate phone number")
    location: str = Field(default="", description="Location")
    linkedin: str = Field(default="", description="LinkedIn URL")
    github: str = Field(default="", description="GitHub URL")
    portfolio: str = Field(default="", description="Portfolio URL")
    target_role: str = Field(..., description="Target job role")
    seniority_level: str = Field(default="Entry-Level", description="Candidate level: Entry, Mid, Senior, Lead")
    professional_summary: str = Field(..., description="3-4 sentence high-impact executive summary with ATS keywords")
    technical_skills: TechnicalSkillsSchema = Field(default_factory=TechnicalSkillsSchema)
    education: str = Field(..., description="Education background description")
    education_items: List[EducationItemSchema] = Field(default_factory=list)
    projects: List[ProjectItemSchema] = Field(default_factory=list)
    experience: List[ExperienceItemSchema] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)
    strengths: List[str] = Field(default_factory=lambda: ["Analytical Problem Solving", "Fast Learning", "Cross-functional Collaboration"])
    ats_keywords: List[str] = Field(default_factory=list, description="Extracted ATS keywords relevant to target role")


class RoadmapStepSchema(BaseModel):
    title: str = Field(..., description="Phase or module title")
    topics: List[str] = Field(default_factory=list, description="Core concepts to master")
    suggested_project: str = Field(default="", description="Hands-on project suggestion")
    recommended_tool: str = Field(default="", description="Framework or library to practice")


class RoadmapDataSchema(BaseModel):
    skill_name: str = Field(..., description="Target skill being learned")
    overview: str = Field(..., description="Brief overview of skill learning path")
    core_milestones: List[RoadmapStepSchema] = Field(default_factory=list)
    secondary_milestones: List[RoadmapStepSchema] = Field(default_factory=list)
    advanced_milestones: List[RoadmapStepSchema] = Field(default_factory=list)
    actionable_tips: List[str] = Field(default_factory=list)


class ChatbotStructuredResponse(BaseModel):
    summary: str = Field(..., description="Direct concise answer summary")
    key_takeaways: List[str] = Field(default_factory=list)
    action_plan: List[str] = Field(default_factory=list)
    recommended_resources: List[str] = Field(default_factory=list)
    followup_questions: List[str] = Field(default_factory=list)


# =====================================================
# JSON PARSER & GEMINI INTEGRATION HELPERS
# =====================================================

def extract_json_from_text(text: str) -> Optional[dict]:
    """
    Safely extract JSON payload from raw model response, handling markdown code fences or conversational text.
    """
    if not text or not isinstance(text, str):
        return None

    cleaned_text = text.strip()

    # Try direct JSON parsing
    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        pass

    # Extract block inside ```json ... ``` or ``` ... ```
    match = re.search(r"```(?:json)?\s*(\{.*\}|\[.*\])\s*```", cleaned_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Extract first outer brace match `{ ... }`
    brace_match = re.search(r"(\{.*\})", cleaned_text, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    return None


def call_gemini_structured(model, prompt: str, schema_class=None):
    """
    Generate structured JSON response using Gemini API with JSON mode or schema parsing fallback.
    """
    if model is None:
        return None

    generation_config = {
        "temperature": 0.2,
        "max_output_tokens": 2048,
        "response_mime_type": "application/json"
    }

    try:
        response = model.generate_content(prompt, generation_config=generation_config)
        raw_text = getattr(response, "text", "")
        parsed_json = extract_json_from_text(raw_text)

        if parsed_json and schema_class:
            try:
                validated_obj = schema_class.model_validate(parsed_json)
                return validated_obj.model_dump()
            except Exception as val_err:
                print(f"Validation warning: {val_err}. Attempting schema reconciliation...")
                if isinstance(parsed_json, dict):
                    normalized = dict(parsed_json)
                    if "basics" in normalized and isinstance(normalized["basics"], dict):
                        b = normalized["basics"]
                        normalized.setdefault("name", b.get("name", ""))
                        normalized.setdefault("email", b.get("email", ""))
                        normalized.setdefault("phone", b.get("phone", ""))
                        normalized.setdefault("professional_summary", b.get("summary", ""))
                    if "summary" in normalized and "professional_summary" not in normalized:
                        normalized["professional_summary"] = normalized["summary"]
                    if "education" in normalized and isinstance(normalized["education"], list):
                        normalized["education"] = "; ".join(str(e) for e in normalized["education"]) if normalized["education"] else "Higher Education"
                    try:
                        return schema_class.model_validate(normalized).model_dump()
                    except Exception as inner_err:
                        print(f"Reconciliation failed: {inner_err}")
                return None
        return parsed_json

    except Exception as exc:
        print(f"Structured Gemini generation failed with JSON mode: {exc}. Retrying without mime type...")
        try:
            # Fallback without response_mime_type
            response = model.generate_content(prompt)
            raw_text = getattr(response, "text", "")
            return extract_json_from_text(raw_text)
        except Exception as retry_err:
            print(f"Fallback Gemini generation failed: {retry_err}")
            return None


# =====================================================
# RESUME FORMATTERS & ATS SCORING ENGINE
# =====================================================

def format_structured_resume_plain_text(data: dict) -> str:
    """
    Converts a structured resume dictionary into an ATS-optimized clean text document.
    """
    lines = []

    # Header
    name = data.get("name", "").strip().upper()
    lines.append(name if name else "CANDIDATE RESUME")
    
    contact_parts = []
    if data.get("email"):
        contact_parts.append(f"Email: {data['email']}")
    if data.get("phone"):
        contact_parts.append(f"Phone: {data['phone']}")
    if data.get("location"):
        contact_parts.append(f"Location: {data['location']}")
    if data.get("linkedin"):
        contact_parts.append(f"LinkedIn: {data['linkedin']}")
    if data.get("github"):
        contact_parts.append(f"GitHub: {data['github']}")
    if data.get("portfolio"):
        contact_parts.append(f"Portfolio: {data['portfolio']}")

    if contact_parts:
        lines.append(" | ".join(contact_parts))
    
    role = data.get("target_role", "")
    if role:
        lines.append(f"Target Role: {role.title()}")
    lines.append("")

    # Summary
    lines.append("PROFESSIONAL SUMMARY:")
    lines.append(data.get("professional_summary", "Dedicated software engineering professional with strong problem solving abilities."))
    lines.append("")

    # Skills
    lines.append("TECHNICAL SKILLS:")
    tech = data.get("technical_skills", {})
    if isinstance(tech, dict):
        if tech.get("programming_languages"):
            lines.append(f"- Programming Languages: {', '.join(tech['programming_languages'])}")
        if tech.get("frameworks_and_libraries"):
            lines.append(f"- Frameworks & Libraries: {', '.join(tech['frameworks_and_libraries'])}")
        if tech.get("databases_and_cloud"):
            lines.append(f"- Databases & Cloud: {', '.join(tech['databases_and_cloud'])}")
        if tech.get("tools_and_platforms"):
            lines.append(f"- Developer Tools & DevOps: {', '.join(tech['tools_and_platforms'])}")
        if tech.get("soft_skills"):
            lines.append(f"- Core Competencies: {', '.join(tech['soft_skills'])}")
    lines.append("")

    # Experience
    lines.append("WORK EXPERIENCE:")
    exp_list = data.get("experience", [])
    if exp_list and isinstance(exp_list, list):
        for exp in exp_list:
            if isinstance(exp, dict):
                r_title = exp.get("role", "Role")
                r_comp = exp.get("company_or_academic", "Organization")
                r_dur = exp.get("duration", "Duration")
                r_loc = exp.get("location", "")
                loc_part = f" | {r_loc}" if r_loc else ""
                lines.append(f"• {r_title} - {r_comp} ({r_dur}){loc_part}")
                for resp in exp.get("key_responsibilities", []):
                    if resp.strip():
                        lines.append(f"  - {resp.strip()}")
    else:
        lines.append("• Hands-on project and academic laboratory experience.")
    lines.append("")

    # Projects
    lines.append("KEY PROJECTS:")
    proj_list = data.get("projects", [])
    if proj_list and isinstance(proj_list, list):
        for proj in proj_list:
            if isinstance(proj, dict):
                p_name = proj.get("name", "Project")
                p_desc = proj.get("description", "")
                p_stack = ", ".join(proj.get("tech_stack", []))
                lines.append(f"• {p_name}")
                if p_desc:
                    lines.append(f"  Description: {p_desc}")
                if p_stack:
                    lines.append(f"  Tech Stack: {p_stack}")
                for ach in proj.get("key_achievements", []):
                    if ach.strip():
                        lines.append(f"  - {ach.strip()}")
    else:
        lines.append("• Portfolio projects available online.")
    lines.append("")

    # Education
    lines.append("EDUCATION:")
    edu_str = data.get("education", "")
    edu_items = data.get("education_items", [])
    if edu_items and isinstance(edu_items, list):
        for edu in edu_items:
            if isinstance(edu, dict):
                deg = edu.get("degree", "Degree")
                inst = edu.get("institution", "Institution")
                yr = edu.get("year", "")
                dtl = edu.get("details", "")
                lines.append(f"• {deg} - {inst} ({yr})")
                if dtl:
                    lines.append(f"  {dtl}")
    elif edu_str:
        lines.append(edu_str)
    else:
        lines.append("Bachelor's Degree in Computer Science / Engineering")
    lines.append("")

    # Certifications & Strengths
    certs = data.get("certifications", [])
    if certs:
        lines.append("CERTIFICATIONS:")
        for cert in certs:
            lines.append(f"- {cert}")
        lines.append("")

    # ATS Keywords
    keywords = data.get("ats_keywords", [])
    if keywords:
        lines.append("ATS RELEVANT KEYWORDS:")
        lines.append(f"- {', '.join(keywords)}")

    return "\n".join(lines)


def calculate_resume_ats_score(resume_data: dict, target_role: str) -> dict:
    """
    Computes an objective, multi-factor ATS Readiness Score for a structured resume:
    1. Keyword coverage against target role requirements (core, secondary, advanced)
    2. Section completeness (Summary, Skills, Experience, Projects, Education)
    3. Action verb and quantification density
    Returns detailed metrics and improvement recommendations.
    """
    from data.role_weights import role_skill_weights

    role_data = role_skill_weights.get(target_role.strip().lower(), {})
    core_skills = set(s.strip().lower() for s in role_data.get("core", []))
    sec_skills = set(s.strip().lower() for s in role_data.get("secondary", []))
    adv_skills = set(s.strip().lower() for s in role_data.get("advanced", []))
    all_role_skills = core_skills.union(sec_skills).union(adv_skills)

    # Collect candidate skills
    candidate_skills = set()
    tech = resume_data.get("technical_skills", {})
    if isinstance(tech, dict):
        for key in ["programming_languages", "frameworks_and_libraries", "databases_and_cloud", "tools_and_platforms"]:
            for item in tech.get(key, []):
                if isinstance(item, str):
                    candidate_skills.add(item.strip().lower())

    # Check skills in full resume text for loose mentions
    resume_full_text = format_structured_resume_plain_text(resume_data).lower()
    for s in all_role_skills:
        if s in resume_full_text:
            candidate_skills.add(s)

    # Keyword match calculations
    matched_core = core_skills.intersection(candidate_skills)
    missing_core = core_skills - candidate_skills

    matched_sec = sec_skills.intersection(candidate_skills)
    missing_sec = sec_skills - candidate_skills

    matched_adv = adv_skills.intersection(candidate_skills)
    missing_adv = adv_skills - candidate_skills

    total_role_skills = len(all_role_skills)
    all_matched = matched_core.union(matched_sec).union(matched_adv)
    all_missing = missing_core.union(missing_sec).union(missing_adv)

    keyword_rate = (len(all_matched) / total_role_skills * 100) if total_role_skills > 0 else 75.0

    # Section completeness scoring (out of 100)
    completeness_score = 0
    section_checks = {
        "Contact Info": bool(resume_data.get("name") and resume_data.get("email")),
        "Professional Summary": len(resume_data.get("professional_summary", "").strip()) >= 50,
        "Technical Skills": len(candidate_skills) >= 4,
        "Work Experience": len(resume_data.get("experience", [])) > 0,
        "Key Projects": len(resume_data.get("projects", [])) > 0,
        "Education": bool(resume_data.get("education") or resume_data.get("education_items")),
    }
    completeness_weight = 100 / len(section_checks)
    for check_passed in section_checks.values():
        if check_passed:
            completeness_score += completeness_weight

    # Action verb check
    action_verbs = ["built", "developed", "architected", "optimized", "implemented", "scaled", "designed", "engineered", "reduced", "increased", "deployed", "spearheaded", "accelerated"]
    action_count = sum(1 for verb in action_verbs if verb in resume_full_text)
    action_score = min(100.0, action_count * 12.5)

    # Overall ATS Score calculation
    # 50% keyword match + 35% completeness + 15% action-verbs
    overall_ats_score = (keyword_rate * 0.50) + (completeness_score * 0.35) + (action_score * 0.15)
    overall_ats_score = round(min(98.5, max(15.0, overall_ats_score)), 1)

    # Improvement recommendations
    recommendations = []
    if missing_core:
        core_list = ", ".join(list(missing_core)[:3])
        recommendations.append(f"Add critical missing core skills: **{core_list}**.")
    if not resume_data.get("projects"):
        recommendations.append("Include at least 2 hands-on technical projects with quantified impact.")
    if action_count < 4:
        recommendations.append("Use stronger impact action verbs (e.g. *Optimized*, *Architected*, *Spearheaded*).")
    if not resume_data.get("linkedin"):
        recommendations.append("Add your LinkedIn profile URL to boost recruiter contact rates.")

    return {
        "ats_score": overall_ats_score,
        "keyword_match_rate": round(keyword_rate, 1),
        "completeness_score": round(completeness_score, 1),
        "action_score": round(action_score, 1),
        "matched_keywords": sorted(list(all_matched)),
        "missing_keywords": sorted(list(all_missing)),
        "matched_core": sorted(list(matched_core)),
        "missing_core": sorted(list(missing_core)),
        "section_checks": section_checks,
        "recommendations": recommendations,
    }
