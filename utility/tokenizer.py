from unidecode import unidecode
from nltk import RegexpTokenizer
from nltk import SnowballStemmer

from nltk.corpus import stopwords

stopwords_en = stopwords.words('english')
stemmer = SnowballStemmer('english')


def tokenize(data, ngram_size):
    data = unidecode(data).strip().lower()

    data = RegexpTokenizer('\w+').tokenize(data)
    res = []

    for x in data:
        if x not in stopwords_en and x.isalpha():
            stemmed = stemmer.stem(x)
            if len(stemmed) >= 3:
                res.append(stemmed)

    final_result = []

    for i in range(0, len(res) - ngram_size + 1):
        ngram = ''
        for j in range(0, ngram_size):
            ngram += res[i + j]
        final_result.append(ngram)

    return final_result
