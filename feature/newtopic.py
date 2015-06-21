from api import FeatureExtractorI


class NewTopic(FeatureExtractorI):
    def __init__(self, train_sample, list_of_attributes, progressbar):
        self.feat_set = set()
        self.list_of_attributes = list_of_attributes
        for _, data, _ in train_sample:
            for attr in self.list_of_attributes:
                for topic in data[attr]:
                    self.feat_set.add(topic)
            progressbar.update(progressbar.currval + 1)

        self.attributes = dict([(x, 'numeric') for x in self.feat_set])

    def extract(self, data):
        topics = []

        for attr in self.list_of_attributes:
            topics.extend(data[attr])

        return {key: 1 for key in topics}
