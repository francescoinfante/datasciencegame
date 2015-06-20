from api import FeatureExtractorI


class IsHD(FeatureExtractorI):
    def __init__(self):
        self.attributes = {'ishd': 'numeric'}

    # return 1 if the video is in hd
    def extract(self, data):
        if data["definition"] == "hd":
            return {'ishd': 1}
