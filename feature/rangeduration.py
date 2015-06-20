from api import FeatureExtractorI


class RangeDuration(FeatureExtractorI):
    def __init__(self, ranges):
        self.attributes = {'range-duration': 'string'}
        self.ranges = ranges

    def extract(self, data):
        old_val = 0
        for max_val in self.ranges:
            if data['duration'] <= max_val:
                return {'range-duration': '%d-%d' % (old_val, max_val)}
            old_val = max_val
        return {'range-duration': '%d-%s' % (old_val, 'Inf')}
