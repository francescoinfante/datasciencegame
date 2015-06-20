class FeatureExtractorI(object):
    def get_attributes(self):
        return self.attributes

    def extract(self, data):
        raise NotImplementedError()
