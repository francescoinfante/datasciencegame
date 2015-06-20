from api import FeatureExtractorI


class CounterFit(FeatureExtractorI):
    def __init__(self):
        self.attributes = {
            'viewCount': 'numeric',
            'likeCount': 'numeric',
            'dislikeCount': 'numeric',
            # 'favoriteCount': 'numeric',
            'commentCount': 'numeric'}

    def extract(self, data):
        return {'viewCount': data['viewCount'], 'likeCount': data['likeCount'], 'dislikeCount': data['dislikeCount'],
                'favoriteCount': data['favoriteCount'], 'commentCount': data['commentCount']}
