from unidecode import unidecode
from nltk import RegexpTokenizer


def tokenize(data):
    data = unidecode(unicode(data, 'utf-8')).strip().lower()
    return RegexpTokenizer('\w+').tokenize(data)
