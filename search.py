from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
import re


def query_process(query):

    # convert the query string to lowercase
    query = query.lower()
    # remove the extra white space
    query = re.sub(r"\s+", " ", query)

    stopwords_english = stopwords.words('english')

    # create the Porter Stemmer
    stemmer = None
    stemmer = PorterStemmer()

    query_tokens = word_tokenize(query)

    clean_tokens = []

    for word in query_tokens:
        if word not in string.punctuation and word not in stopwords_english:
            stem_word = []
            # stem the tokens
            stem_word = stemmer.stem(word)
            clean_tokens.append(stem_word)

    return clean_tokens
