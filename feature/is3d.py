from api import FeatureExtractorI


class Is3D(FeatureExtractorI):
    def __init__(self):
        self.attributes = {'is3d': 'numeric'}

    #return 1 if the video is in 3d
    def extract(self, data):
        if(data["dimension"] == "3d"):
            return {'is3d': 1}


