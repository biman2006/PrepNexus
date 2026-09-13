import streamlit as st
import string
import re


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

    "node": "node",
    "nodejs": "nodejs",
    "node js": "nodejs",
    "node.js": "nodejs",

    "react": "react",
    "reactjs": "react",
    "react js": "react",
    "react.js": "react",

    "next": "nextjs",
    "next.js": "nextjs",
    "next js": "nextjs",
    "nextjs": "nextjs",

    "express": "expressjs",
    "express.js": "expressjs",
    "express js": "expressjs",
    "expressjs": "expressjs",

    "vue": "vuejs",
    "vue.js": "vuejs",
    "vue js": "vuejs",
    "vuejs": "vuejs",

    "ci/cd": "ci cd",
    "ci cd": "ci cd",

    "c++": "c++",
    "cpp": "c++",
    "c#": "c#",
    "csharp": "c#",
    ".net": "dotnet",
    "dotnet": "dotnet",

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
    - Preserve special language tokens (c++, c#, .net)
    - Replace hyphens/underscores with spaces
    - Standardize aliases
    - Clean remaining punctuation
    """
    text = text.lower()

    # Protect key programming language symbols
    text = re.sub(r"\bc\+\+\b", " cpp_token ", text)
    text = re.sub(r"\bc#\b", " csharp_token ", text)
    text = re.sub(r"\b\.net\b", " dotnet_token ", text)

    # Replace separators
    text = text.replace("-", " ").replace("_", " ").replace("/", " ")

    # Alias replacements
    replacements = {
        "sklearn": "scikit learn",
        "powerbi": "power bi",
        "node js": "nodejs",
        "react js": "reactjs",
        " ml ": " machine learning ",
        " dl ": " deep learning ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # Remove punctuation except alphanumeric and space
    text = re.sub(r"[^\w\s]", " ", text)

    # Restore preserved tokens
    text = text.replace("cpp_token", "c++")
    text = text.replace("csharp_token", "c#")
    text = text.replace("dotnet_token", "dotnet")

    return " ".join(text.split())


# =====================================================
# NORMALIZE SKILL NAME
# =====================================================
def normalize_skill(skill):
    """
    Normalize individual skill names
    and map aliases to standardized versions.
    """
    s = skill.lower().strip()
    if s in ("c++", "cpp"):
        return "c++"
    if s in ("c#", "csharp"):
        return "c#"
    if s in (".net", "dotnet"):
        return "dotnet"

    normalized = (
        s.replace("-", " ")
        .replace("_", " ")
        .replace(".", " ")
        .replace("/", " ")
        .strip()
    )

    # Alias standardization
    aliased = SKILL_ALIASES.get(
        normalized,
        normalized
    )

    return " ".join(aliased.split())


# =====================================================
# PREPROCESS SKILL LIST
# =====================================================
@st.cache_data
def preprocess_skill_list(skill_list):
    """
    Normalize + sort skills once for performance.
    """

    normalized_skills = list(
        set(
            normalize_skill(skill)
            for skill in skill_list
        )
    )

    return sorted(
        normalized_skills,
        key=len,
        reverse=True
    )


# =====================================================
# SKILL EXTRACTION
# =====================================================
@st.cache_data
def extract_skill(text, skill_list):
    """
    Extract matching skills from resume/job text
    using robust normalized matching.
    """

    found_skills = set()

    # Normalize text
    normalized_text = normalize_text(text)

    # Tokenize
    words = set(
        normalized_text.split()
    )

    # Preprocessed skills
    sorted_skills = preprocess_skill_list(
        tuple(skill_list)
    )

    # =================================================
    # SKILL MATCHING
    # =================================================
    for skill in sorted_skills:

        # Multi-word skill
        if " " in skill:

            if skill in normalized_text:
                found_skills.add(skill)

        # Single-word skill
        else:

            if skill in words:
                found_skills.add(skill)

    # =================================================
    # RETURN CLEAN LIST
    # =================================================
    return list(found_skills)