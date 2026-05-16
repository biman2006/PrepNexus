import string


# =====================================================
# SKILL ALIAS MAPPING
# =====================================================
SKILL_ALIASES = {
    # Data Science / ML
    "scikit learn": "scikit learn",
    "sklearn": "scikit learn",
    "scikit-learn": "scikit learn",
    

    "machine learning": "machine learning",
    "ml": "machine learning",

    "deep learning": "deep learning",
    "dl": "deep learning",

    "tensorflow": "tensorflow",
    "tf": "tensorflow",

    "pytorch": "pytorch",
    "torch": "pytorch",

    "powerbi": "power bi",
    "power bi": "power bi",

    "tableau desktop": "tableau",
    "tableau": "tableau",

    "numpy": "numpy",
    "np": "numpy",

    "pandas": "pandas",
    "pd": "pandas",

    # Web Development
    "javascript": "javascript",
    "js": "javascript",

    "nodejs": "nodejs",
    "node js": "nodejs",

    "reactjs": "react",
    "react js": "react",

    # Cloud
    "aws": "amazon web services",
    "amazon web services": "amazon web services",

    "gcp": "google cloud platform",
    "google cloud": "google cloud platform",
}


# =====================================================
# NORMALIZE TEXT
# =====================================================
def normalize_text(text):
    """
    Normalize full resume/job text for better matching:
    - Lowercase
    - Replace hyphens/underscores with spaces
    - Standardize aliases
    - Remove punctuation
    """

    text = text.lower()

    # Replace separators
    text = text.replace("-", " ").replace("_", " ")

    # Alias replacements inside resume text
    text = text.replace("sklearn", "scikit learn")
    text = text.replace("powerbi", "power bi")
    text = text.replace("node js", "nodejs")
    text = text.replace("react js", "reactjs")
    text = text.replace("js", "javascript")
    text = text.replace("ml", "machine learning")
    text = text.replace("dl", "deep learning")

    # Remove punctuation
    text = text.translate(
        str.maketrans('', '', string.punctuation)
    )

    return text


# =====================================================
# NORMALIZE SKILL NAME
# =====================================================
def normalize_skill(skill):
    """
    Normalize individual skill names
    and map aliases to standardized versions.
    """

    normalized = (
        skill.lower()
        .replace("-", " ")
        .replace("_", " ")
        .strip()
    )

    # Get the aliased version
    aliased = SKILL_ALIASES.get(normalized, normalized)
    
    # Convert hyphens to spaces to match normalize_text output
    aliased = aliased.replace("-", " ").strip()
    
    return aliased


# =====================================================
# SKILL EXTRACTION
# =====================================================
def extract_skill(text, skill_list):
    """
    Extract matching skills from resume text
    using robust normalized matching.
    """

    found_skills = []

    # Normalize input text
    normalized_text = normalize_text(text)

    # Tokenize words
    words = set(normalized_text.split())

    # Sort skills by length so longer skills match first
    sorted_skills = sorted(
        skill_list,
        key=len,
        reverse=True
    )

    # =================================================
    # SKILL MATCHING
    # =================================================
    for skill in sorted_skills:

        normalized_skill = normalize_skill(skill)

        # Multi-word skill
        if " " in normalized_skill:

            if normalized_skill in normalized_text:
                found_skills.append(normalized_skill)

        # Single-word skill
        else:

            if normalized_skill in words:
                found_skills.append(normalized_skill)

    # =================================================
    # REMOVE DUPLICATES
    # =================================================
    return list(set(found_skills))