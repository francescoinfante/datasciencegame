import langid

from api import FeatureExtractorI


class LangID(FeatureExtractorI):
    def __init__(self, sample):
        type = []
        for _, x, _ in sample:
            language = langid.classify(x['title'] + ' ' + x['description'])[0]
            type.append(language)
        self.attributes = {}
        for x in type:
            self.attributes[x] = 'numeric'

    def extract(self, data):
        language = langid.classify(data['title'] + ' ' + data['description'])[0]
        print language
        return {language: 1}
