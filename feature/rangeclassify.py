from api import FeatureExtractorI


class RangeClassify(FeatureExtractorI):
    def __init__(self, feat_name, ranges):
        self.attributes = {}
        self.feat_name = str(feat_name)
        self.ranges = ranges
        for x in self.ranges:
            self.attributes['range-' + str(feat_name) + str(x)] = 'numeric'

    def extract(self, data):
        for max_val in self.ranges:
            if data[self.feat_name] <= max_val:
                return {'range-' + str(self.feat_name) + str(max_val): 1}

        return {'range-' + str(self.feat_name) + 'more': 1}
