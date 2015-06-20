from api import FeatureExtractorI


class HasCaption(FeatureExtractorI):
    def __init__(self):
        self.attributes = {'hascaption': 'numeric'}

    #True if the video has caption
    def extract(self, data):
        if(data["hascaption"]):
            return {'hascaption': 1}