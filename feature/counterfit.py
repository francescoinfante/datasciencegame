from api import FeatureExtractorI


class CounterFit(FeatureExtractorI):
    def __init__(self):
        self.attributes = {'viewCount': 'numeric'}
        self.attributes = {'likeCount': 'numeric'}
        self.attributes = {'dislikeCount': 'numeric'}
        self.attributes = {'favoriteCount': 'numeric'}
        self.attributes = {'commentCount': 'numeric'}

    # return 1 if the video is in 3d
    def extract(self, data):
        return {'viewCount': data['viewCount'], 'likeCount': data['likeCount'], 'dislikeCount': data['dislikeCount'],
                'favoriteCount': data['favoriteCount'], 'commentCount': data['commentCount']}
