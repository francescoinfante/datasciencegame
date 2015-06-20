from api import FeatureExtractorI
from collections import Counter
from nltk.stem.snowball import SnowballStemmer
from nltk.parse import stanford
from feature.api import FeatureExtractorI


class BagOfWordsOfTitle(FeatureExtractorI):
    def __init__(self, train_sample):
        self.token_set = set()
        for _, given_features, _ in train_sample:
            self.token_set |= set(tokenize(given_features['title']))

        self.attributes = dict([(x, 'numeric') for x in self.token_set])

    def extract(self, data):
        tokens = tokenize(data['title'])

        return dict(Counter(tokens))
