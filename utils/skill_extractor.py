import string

def extract_skill(text, skill_list):
    found_skill = []

    # Lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(
        str.maketrans('', '', string.punctuation)
    )

    # Tokenize
    words = set(text.split())

    # Sort longer skills first
    sorted_skills = sorted(
        skill_list,
        key=len,
        reverse=True
    )

    for skill in sorted_skills:

        skill_lower = skill.lower()

        # Multi-word skill
        if " " in skill_lower:
            if skill_lower in text:
                found_skill.append(skill_lower)

        # Single-word skill
        else:
            if skill_lower in words:
                found_skill.append(skill_lower)

    return list(set(found_skill))