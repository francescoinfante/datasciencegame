from unidecode import unidecode
from nltk import RegexpTokenizer
from nltk import SnowballStemmer

from nltk.corpus import stopwords

stopwords_en = stopwords('english')
stemmer = SnowballStemmer('english')


def tokenize(data):
    data = unidecode(data).strip().lower()

    data = RegexpTokenizer('\w+').tokenize(data)

    res = []

    for x in data:
        if x not in stopwords:
            res.append(stemmer.stem(x))

    return res
