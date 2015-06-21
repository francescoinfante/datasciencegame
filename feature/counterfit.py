from api import FeatureExtractorI


class CounterFit(FeatureExtractorI):
    def __init__(self, train_sample, test_sample):
        maximums = {'viewCount': 1, 'likeCount': 1, 'dislikeCount': 1, 'favoriteCount': 1, 'commentCount': 1}
        for instance in train_sample + test_sample:
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
        view_count = float(data['viewCount']) / self.maximums['viewCount'] if data['viewCount'] != 0 else 0
        like_count = float(data['likeCount']) / self.maximums['likeCount'] if data['likeCount'] != 0 else 0
        dislike_count = float(data['dislikeCount']) / self.maximums['dislikeCount'] if data['dislikeCount'] != 0 else 0
        favorite_count = float(data['favoriteCount']) / self.maximums['favoriteCount'] \
            if data['favoriteCount'] != 0 else 0
        comment_count = float(data['commentCount']) / self.maximums['commentCount'] if data['commentCount'] != 0 else 0

        return {'viewCount': view_count, 'likeCount': like_count, 'dislikeCount': dislike_count,
                'favoriteCount': favorite_count, 'commentCount': comment_count}
