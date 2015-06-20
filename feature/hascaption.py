from api import FeatureExtractorI


class HasCaption(FeatureExtractorI):
    def __init__(self):
        self.attributes = {'caption': 'numeric'}

    # True if the video has caption
    def extract(self, data):
        if data["caption"]:
            return {'caption': 1}
        return {}
