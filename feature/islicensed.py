from api import FeatureExtractorI


class IsLicensed(FeatureExtractorI):
    def __init__(self):
        self.attributes = {'islicensed': 'numeric'}

    # True if is a licensed content
    def extract(self, data):
        if data["licensedContent"]:
            return {'islicensed': 1}
