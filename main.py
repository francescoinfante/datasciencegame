import logging
import csv

from utility import array_to_dict

DEFAULT_TRAINING_INPUT = '../input/train_sample.csv'
DEFAULT_TEST_INPUT = '../input/test_sample.csv'

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    possible_categories = set()
    train_sample = []  # list of tuples: '0', 'dict', 'category'
    test_sample = []  # list of tuples: 'test_id', 'dict', 'random_category'

    """
    Train Sample CSV header

    "video_category_id","title","description","published_at","viewCount","likeCount","dislikeCount","favoriteCount",
    "commentCount","duration","dimension","definition","caption","licensedContent","topicIds","relevantTopicIds"
    """

    with open(DEFAULT_TRAINING_INPUT, 'r') as f:
        f.next()
        csv_reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in csv_reader:
            category = row[0]
            possible_categories.add(category)
            if category == '':
                print "hello"
            train_sample.append(('0', array_to_dict(row[1:]), category))

    """
    Test Sample CSV header

    id,"title","title","description","published_at","viewCount","likeCount","dislikeCount","favoriteCount",
    "commentCount","duration","dimension","definition","caption","licensedContent","topicIds","relevantTopicIds"
    """

    with open(DEFAULT_TEST_INPUT, 'r') as f:
        f.next()
        csv_reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in csv_reader:
            test_id = row[0]
            test_sample.append((test_id, array_to_dict(row[1:]), '0'))

    print possible_categories
