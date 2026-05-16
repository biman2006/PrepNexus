from utils.skill_extractor import normalize_skill


def calculate_readiness(resume_skills, role_data):
    """
    Calculates weighted readiness score with normalized skill matching.
    Ensures aliases like:
    - scikit-learn
    - scikit learn
    - sklearn
    all match correctly.
    """

    # =====================================================
    # NORMALIZE RESUME SKILLS
    # =====================================================
    normalized_resume_skills = set(
        normalize_skill(skill)
        for skill in resume_skills
    )

    # =====================================================
    # NORMALIZE ROLE SKILLS
    # =====================================================
    core = set(
        normalize_skill(skill)
        for skill in role_data["core"]
    )

    secondary = set(
        normalize_skill(skill)
        for skill in role_data["secondary"]
    )

    advanced = set(
        normalize_skill(skill)
        for skill in role_data["advanced"]
    )

    # =====================================================
    # SCORE CALCULATIONS
    # =====================================================
    core_score = (
        len(core.intersection(normalized_resume_skills)) / len(core)
    ) * 60 if core else 0

    secondary_score = (
        len(secondary.intersection(normalized_resume_skills)) / len(secondary)
    ) * 30 if secondary else 0

    advanced_score = (
        len(advanced.intersection(normalized_resume_skills)) / len(advanced)
    ) * 10 if advanced else 0

    # =====================================================
    # FINAL READINESS
    # =====================================================
    final_score = core_score + secondary_score + advanced_score

    # =====================================================
    # RETURN STRUCTURED RESULTS
    # =====================================================
    return {
        "core_matched": core.intersection(normalized_resume_skills),
        "secondary_matched": secondary.intersection(normalized_resume_skills),
        "advanced_matched": advanced.intersection(normalized_resume_skills),

        "missing_core": core - normalized_resume_skills,
        "missing_secondary": secondary - normalized_resume_skills,
        "missing_advanced": advanced - normalized_resume_skills,

        "core_score": round(core_score, 2),
        "secondary_score": round(secondary_score, 2),
        "advanced_score": round(advanced_score, 2),

        "readiness_score": round(final_score, 2)
    }