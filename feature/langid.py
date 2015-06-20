from api import FeatureExtractorI

import langid


class LangID(FeatureExtractorI):
    def __init__(self, sample):
        type = []
        for x in sample:
            language = langid.classify(sample['title'] + ' ' + sample['description'])[0]
            type.append(language)
        self.attributes = {'lang': '{' + ','.join(type) + '}'}

    def extract(self, data):
        language = langid.classify(data['title'] + ' ' + data['description'])[0]
        return {'lang': 'language'}
