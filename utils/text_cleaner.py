import string

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
except ImportError as exc:
    raise ImportError(
        "NLTK is required for text cleaning. Install it with: pip install nltk"
    ) from exc

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

stop_words = set(stopwords.words("english"))

def clean_text(text):

    #lower_case 
    text=text.lower()

    #Remove punctuation (except hyphens and underscores for skill names like scikit-learn, node.js, c++)
    punctuation_to_remove = string.punctuation.replace('-', '').replace('_', '')
    text=text.translate(str.maketrans('','',punctuation_to_remove))

    #Tokenize

    words=word_tokenize(text)

    #remove stopwords 

    filtered_words=[word for word in words if word not in stop_words]

    #join back to string 
    cleand_text=" ".join(filtered_words)

    return cleand_text

