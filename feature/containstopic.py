from api import FeatureExtractorI


class ContainsTopic(FeatureExtractorI):
    def __init__(self, train_sample):
        self.attributes = {}
        for (_, given_features, _) in train_sample:
            self.attributes.update({key: 'numeric' for key in given_features['topicIds']})

    def extract(self, data):
        return {key: '1' for key in data['topicIds']}
