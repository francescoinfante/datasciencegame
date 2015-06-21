import langid

from api import FeatureExtractorI


class LangID(FeatureExtractorI):
    def __init__(self, sample):
        type = []
        for x in sample:
            language = langid.classify(sample['title'] + ' ' + sample['description'])[0]
            type.append(language)
        self.attributes = {}
        for x in type:
            self.attributes[x] = 'numeric'

    def extract(self, data):
        language = langid.classify(data['title'] + ' ' + data['description'])[0]
        return {language: 1}
