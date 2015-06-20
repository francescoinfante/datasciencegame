from api import FeatureExtractorI


class RangeClassify(FeatureExtractorI):
    def __init__(self, feat_name, ranges):
        self.attributes = {'range-' + str(feat_name): 'string'}
        self.feat_name = str(feat_name)
        self.ranges = ranges

    def extract(self, data):
        old_val = 0
        for max_val in self.ranges:
            if data[self.feat_name] <= max_val:
                return {'range-' + self.feat_name: '%d-%d' % (old_val, max_val)}
            old_val = max_val
        return {'range-' + self.feat_name: '%d-%s' % (old_val, 'Inf')}
