import logging
import csv
from argparse import ArgumentParser

from progressbar import ProgressBar

import feature
from arffbuilder import arff_sparse_builder

from utility import array_to_dict

DEFAULT_TRAINING_INPUT = 'input/train_sample.csv'
DEFAULT_TEST_INPUT = 'input/test_sample.csv'
DEFAULT_CONFIGURATION = 'input/configure.cfg'

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    argparser = ArgumentParser(description='DSG')
    argparser.add_argument('-i1', '--training-input', default=DEFAULT_TRAINING_INPUT,
                           help='training input file (csv format)')
    argparser.add_argument('-i2', '--test-input', default=DEFAULT_TEST_INPUT,
                           help='test input file (csv format)')
    argparser.add_argument('-c', '--configuration', default=DEFAULT_CONFIGURATION,
                           help='configuration file')
    args = argparser.parse_args()

    possible_categories = set()
    train_sample = []  # list of tuples: '0', 'dict', 'category'
    test_sample = []  # list of tuples: 'test_id', 'dict', 'random_category'

    """
    Train Sample CSV header

    "video_category_id","title","description","published_at","viewCount","likeCount","dislikeCount","favoriteCount",
    "commentCount","duration","dimension","definition","caption","licensedContent","topicIds","relevantTopicIds"
    """

    with open(args.training_input, 'r') as f:
        f.next()
        csv_reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in csv_reader:
            category = row[0]
            possible_categories.add(category)
            train_sample.append(('0', array_to_dict(row[1:]), category))

    """
    Test Sample CSV header

    id,"title","title","description","published_at","viewCount","likeCount","dislikeCount","favoriteCount",
    "commentCount","duration","dimension","definition","caption","licensedContent","topicIds","relevantTopicIds"
    """

    with open(args.test_input, 'r') as f:
        f.next()
        csv_reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in csv_reader:
            test_id = row[0]
            test_sample.append((test_id, array_to_dict(row[1:]), '0'))

    """
    Call init for each plugin in the configuration file
    """

    plugins = []
    with open(args.configuration) as f:
        plugins_calls = []
        for plugin in f:
            plugin = plugin.rstrip().lstrip()
            if plugin and not plugin.startswith('#'):
                plugin = 'feature.' + plugin
                try:
                    plugins_calls.append(compile(plugin, '<string>', 'eval'))
                except SyntaxError:
                    logging.error('Syntax error: ' + plugin)

        progressbar = ProgressBar(maxval=len(plugins_calls) * len(train_sample)).start()
        for i in range(len(plugins_calls)):
            plugins.append(eval(plugins_calls[i]))
            progressbar.update((i + 1) * len(train_sample))
        progressbar.finish()

    """
    Get all the attributes from each plugin (dictionary key: 'plugin_name:attribute_name', value: 'attribute_type')
    """

    attributes = feature.get_attributes(plugins, possible_categories)

    """
    Build actual arff files
    """

    train_data = feature.extract_features(plugins, train_sample)

    arff_sparse_builder(args.training_output, 'train_set', attributes, train_data)

    logging.info(args.training_output + ' is ready!')

    test_data = feature.extract_features(plugins, test_sample)
    arff_sparse_builder(args.test_output, 'test_set', attributes, test_data)

    logging.info(args.test_output + ' is ready!')
