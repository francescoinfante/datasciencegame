from unidecode import unidecode
from nltk import RegexpTokenizer


def tokenize(data):
    data = unidecode(data).strip().lower()
    return RegexpTokenizer('\w+').tokenize(data)
