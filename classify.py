from argparse import ArgumentParser
import csv
import logging
from os.path import join
from os.path import dirname
from sklearn import cross_validation, svm, naive_bayes
from sklearn.feature_selection import SelectKBest, chi2

from utility.arfftoscikit import get_vector_from

DEFAULT_OUTPUT = join(dirname(__file__), 'output/result-scikit.csv')
DEFAULT_TRAIN_SET = join(dirname(__file__), 'output/output_train.arff')
DEFAULT_TEST_SET = join(dirname(__file__), 'output/output_test.arff')
DEFAULT_FEATURES_RANKING = join(dirname(__file__), 'output/features_ranking.csv')

logging.basicConfig()
LOGGER = logging.getLogger('Classify')
LOGGER.setLevel(logging.INFO)


def compute_max(x, maximums, features_types):
    non_zero_indexes = x.nonzero()
    for (i, j) in zip(non_zero_indexes[0], non_zero_indexes[1]):
        if features_types == 'numeric':
            maximums[j] = max(x[i, j], maximums[j])


def normalize(x, maximums, features_types):
    non_zero_indexes = x.nonzero()
    for (i, j) in zip(non_zero_indexes[0], non_zero_indexes[1]):
        if features_types == 'numeric':
            x[i, j] /= maximums[j]


def do_not_call_it():
    svm.LinearSVC()
    naive_bayes.MultinomialNB()
    naive_bayes.GaussianNB()


def main(train_set, test_set, output_file, validate=False, k=5, num_of_features=0):
    """

    :param train_set:
    :param test_set:
    :param output_file:
    :param validate:
    :param k:
    :return:
    """

    """
    Reading configuration
    """

    executor_calls = []
    with open('input/classifier.cfg') as f:
        for executor in f:
            executor = executor.rstrip().lstrip()
            if executor and not executor.startswith('#'):
                try:
                    executor_calls.append(compile(executor, '<string>', 'eval'))
                except SyntaxError:
                    LOGGER.error('Syntax error: ' + executor)

    if len(executor_calls) != 1:
        LOGGER.error('Not a single classifier is specified')
        exit()

    """
    Input
    """

    LOGGER.info('Reading training set...')
    with open(train_set, 'r') as f:
        (_, train_features, classes, features_names, features_types) = get_vector_from(f)

    LOGGER.info('Reading test set...')
    with open(test_set, 'r') as f:
        (ids, test_features, _, _, _) = get_vector_from(f)

    """
    Normalization
    """

    LOGGER.info('Normalizing...')

    # one_hot_encoder = preprocessing.OneHotEncoder(categorical_features=[x[0] == '{' for x in features_types])
    # one_hot_encoder.fit(train_features)
    # train_features = one_hot_encoder.transform(train_features)
    # test_features = one_hot_encoder.transform(test_features)

    maximums = [1] * len(features_names)
    compute_max(train_features, maximums, features_types)
    compute_max(test_features, maximums, features_types)
    normalize(train_features, maximums, features_types)
    normalize(test_features, maximums, features_types)

    # dense_train_features = train_features.toarray()
    # dense_test_features = test_features.toarray()
    # scaler = preprocessing.MinMaxScaler().fit(dense_train_features)
    # scaler.transform(dense_train_features)
    # scaler.transform(dense_test_features)
    # normalizer = preprocessing.Normalizer().fit(train_features)
    # train_features = normalizer.transorm(train_features)
    # test_features = normalizer.transorm(test_features)

    """
    Feature selection
    """

    if num_of_features > 0:
        features_ranker = SelectKBest(chi2, k=num_of_features).fit(train_features, classes)
        features_ranker.transform(train_features)
        features_ranker.transform(test_features)

        with open(DEFAULT_FEATURES_RANKING, 'w') as f:
            csv_writer = csv.writer(f, delimiter=';')
            scores = zip(features_ranker.scores_, features_names)
            for (score, name) in sorted(scores, reverse=True):
                csv_writer.writerow([name, score])

    """
    Validation
    """

    if validate:
        LOGGER.info('Validating...')
        eval_clf = eval(executor_calls[0])
        cv = cross_validation.cross_val_score(eval_clf, train_features, classes, cv=k)
        print 'Accuracy: %f' % cv.mean()

    """
    Training
    """

    LOGGER.info('Training classifier...')
    clf = eval(executor_calls[0])
    clf.fit(train_features, classes)

    """
    Predictions
    """

    LOGGER.info('Computing predictions...')
    predictions = zip(ids, clf.predict(test_features))

    """
    Output
    """

    LOGGER.info('Writing results...')
    with open(output_file, 'w') as f:
        csv_writer = csv.writer(f, delimiter=';')
        csv_writer.writerow(['id', 'video_category_id'])
        for (instance_id, prediction) in sorted(predictions):
            csv_writer.writerow([instance_id, prediction])


if __name__ == '__main__':
    argparser = ArgumentParser(description='Classify by SVM.')
    argparser.add_argument('-i1', '--train-input', default=DEFAULT_TRAIN_SET,
                           help='training input file (arff)')
    argparser.add_argument('-i2', '--test-input', default=DEFAULT_TEST_SET,
                           help='test input file (arff)')
    argparser.add_argument('-o', '--output', default=DEFAULT_OUTPUT,
                           help='output file (csv)')
    argparser.add_argument('-v', '--validate', action='store_true', default=False,
                           help='output file (csv)')
    argparser.add_argument('-k', '--k-folds', default=5,
                           help='number of folds in the k-folds cross validation')
    argparser.add_argument('-n', '--num-of-features', default=0, type=int,
                           help='number of features to use')
    args = argparser.parse_args()

    main(args.train_input, args.test_input, args.output, validate=args.validate, k=args.k_folds,
         num_of_features=args.num_of_features)
