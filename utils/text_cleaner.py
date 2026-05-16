import string

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
except ImportError as exc:
    raise ImportError(
        "NLTK is required for text cleaning. Install it with: pip install nltk"
    ) from exc


# =====================================================
# ENSURE REQUIRED NLTK DATA
# =====================================================
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords", quiet=True)


# =====================================================
# STOPWORDS
# =====================================================
stop_words = set(
    stopwords.words("english")
)


# =====================================================
# CLEAN TEXT FUNCTION
# =====================================================
def clean_text(text):
    """
    Cleans resume text while preserving
    important technical skill formatting.
    """

    # Lowercase
    text = text.lower()

    # Remove punctuation
    # Preserve hyphens + underscores
    punctuation_to_remove = (
        string.punctuation
        .replace('-', '')
        .replace('_', '')
    )

    text = text.translate(
        str.maketrans(
            '',
            '',
            punctuation_to_remove
        )
    )

    # Tokenize
    words = word_tokenize(text)

    # Remove stopwords
    filtered_words = [
        word for word in words
        if word not in stop_words
    ]

    # Join back
    cleaned_text = " ".join(filtered_words)

    return cleaned_text