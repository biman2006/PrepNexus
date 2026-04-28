import nltk
import string
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

nltk.download('punkt_tab')
nltk.download('stopwords')

stop_words=set(stopwords.words("english"))
def clean_text(text):

    #lower_case 
    text=text.lower()

    #Remove punctuation

    text=text.translate(str.maketrans('','',string.punctuation))

    #Tokenize

    words=word_tokenize(text)

    #remove stopwords 

    filtered_words=[word for word in words if word not in stop_words]

    #join back to string 
    cleand_text=" ".join(filtered_words)

    return cleand_text

