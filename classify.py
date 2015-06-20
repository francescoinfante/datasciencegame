from argparse import ArgumentParser
import csv
import logging
from os.path import join
from os.path import dirname
from sklearn import cross_validation, svm, naive_bayes

from utility.arfftoscikit import get_vector_from

DEFAULT_OUTPUT = join(dirname(__file__), 'output/result-scikit.csv')
DEFAULT_TRAIN_SET = join(dirname(__file__), 'output/output_train.arff')
DEFAULT_TEST_SET = join(dirname(__file__), 'output/output_test.arff')

logging.basicConfig()
LOGGER = logging.getLogger('Classify')
LOGGER.setLevel(logging.INFO)


def do_not_call_it():
    svm.LinearSVC()
    naive_bayes.MultinomialNB()
    naive_bayes.GaussianNB()


def main(train_set, test_set, output_file, validate=False, k=5, num_of_features=-1):
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
        (_, train_features, classes) = get_vector_from(f)

    LOGGER.info('Reading test set...')
    with open(test_set, 'r') as f:
        (ids, test_features, _) = get_vector_from(f)

    """
    Feature selection
    """

    # features_ranker = SelectKBest(chi2, k=2).fit(train_features, classes)

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
    argparser.add_argument('-n', '--num-of-features', default=False,
                           help='whether to normalise the data')
    args = argparser.parse_args()

    main(args.train_input, args.test_input, args.output, validate=args.validate, k=args.k_folds,
         num_of_features=args.num_of_features)
