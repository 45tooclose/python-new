from nltk.tokenize import word_tokenize,sent_tokenize
from TextCleaner import TextCleaner
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

"""
Using lemmatizaiton
returns tokenized words in a list

"""
def lemmatize(text):


    wnl = WordNetLemmatizer()

    tc=TextCleaner(txt=text)
    tc.clear_text_base()
    tc.clear_special_char()
    text=tc.get_text()

    words = word_tokenize(text)
    filtered_sentence = []
    stop_words = set(stopwords.words("english"))

    for w in words:
        if w not in stop_words:
            filtered_sentence.append(w)

    lemmatized=[]

    for w in filtered_sentence:
        lemmatized.append(wnl.lemmatize(w))

    return lemmatized

