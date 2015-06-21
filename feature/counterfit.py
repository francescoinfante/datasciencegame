from api import FeatureExtractorI


class CounterFit(FeatureExtractorI):
    def __init__(self, train_sample, test_sample, normalize=False):
        self.normalize = normalize
        if normalize:
            maximums = {'viewCount': 1, 'likeCount': 1, 'dislikeCount': 1, 'favoriteCount': 1, 'commentCount': 1}
            for instance in zip(*train_sample)[1] + zip(*test_sample)[1]:
                maximums['viewCount'] = max(maximums['viewCount'], instance['viewCount'])
                maximums['likeCount'] = max(maximums['likeCount'], instance['likeCount'])
                maximums['dislikeCount'] = max(maximums['dislikeCount'], instance['dislikeCount'])
                maximums['favoriteCount'] = max(maximums['favoriteCount'], instance['favoriteCount'])
                maximums['commentCount'] = max(maximums['commentCount'], instance['commentCount'])
            self.maximums = maximums

        self.attributes = {
            'viewCount': 'numeric',
            'likeCount': 'numeric',
            'dislikeCount': 'numeric',
            # 'favoriteCount': 'numeric',
            'commentCount': 'numeric'}

    def extract(self, data):
        if self.normalize:
            view_count = float(data['viewCount']) / self.maximums['viewCount']
            like_count = float(data['likeCount']) / self.maximums['likeCount']
            dislike_count = float(data['dislikeCount']) / self.maximums['dislikeCount']
            favorite_count = float(data['favoriteCount']) / self.maximums['favoriteCount']
            comment_count = float(data['commentCount']) / self.maximums['commentCount']
        else:
            view_count = data['viewCount']
            like_count = data['likeCount']
            dislike_count = data['dislikeCount']
            favorite_count = data['favoriteCount']
            comment_count = data['commentCount']

        return {'viewCount': view_count, 'likeCount': like_count, 'dislikeCount': dislike_count,
                'favoriteCount': favorite_count, 'commentCount': comment_count}
