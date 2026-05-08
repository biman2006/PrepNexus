import string


def normalize_text(text):
    """
    Normalize text for better skill matching:
    - Lowercase
    - Replace hyphens/underscores with spaces
    - Remove punctuation
    """

    text = text.lower()

    text = text.replace(
        "-",
        " "
    ).replace(
        "_",
        " "
    )

    text = text.translate(
        str.maketrans(
            '',
            '',
            string.punctuation
        )
    )

    return text


def normalize_skill(skill):
    """
    Normalize individual skill names.
    """

    return (
        skill.lower()
        .replace("-", " ")
        .replace("_", " ")
        .strip()
    )


def extract_skill(
    text,
    skill_list
):
    """
    Extracts matching skills from resume text
    with normalized matching.
    """

    found_skill = []

    # =================================================
    # NORMALIZE RESUME TEXT
    # =================================================
    normalized_text = normalize_text(
        text
    )

    words = set(
        normalized_text.split()
    )

   
    sorted_skills = sorted(
        skill_list,
        key=len,
        reverse=True
    )

    
    # SKILL MATCHING
    
    for skill in sorted_skills:

        skill_lower = normalize_skill(
            skill
        )

        # Multi-word skills
        if " " in skill_lower:

            if skill_lower in normalized_text:
                found_skill.append(
                    skill_lower
                )

        # Single-word skills
        else:

            if skill_lower in words:
                found_skill.append(
                    skill_lower
                )


    # REMOVE DUPLICATES

    return list(
        set(found_skill)
    )