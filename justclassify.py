from argparse import ArgumentParser
import csv
import logging
from os.path import join
from os.path import dirname
from sklearn.externals import joblib
from sklearn import svm, naive_bayes
from sklearn import ensemble
from sklearn.multiclass import OneVsRestClassifier

# import matplotlib.pyplot as plt
from utility.arfftoscikit import get_vector_from

DEFAULT_OUTPUT = join(dirname(__file__), 'output/result-scikit.csv')
DEFAULT_TRAIN_SET = join(dirname(__file__), 'output/output_train.arff')
DEFAULT_TEST_SET = join(dirname(__file__), 'output/output_test.arff')
DEFAULT_FEATURES_RANKING = join(dirname(__file__), 'output/features_ranking.csv')
DEFAULT_MODEL_FILE = join(dirname(__file__), 'output/model.dat')
DEFAULT_SELECTOR_FILE = join(dirname(__file__), 'output/selector.dat')

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s')
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def do_not_call_it():
    svm.LinearSVC()
    naive_bayes.MultinomialNB()
    naive_bayes.GaussianNB()
    ensemble.RandomForestClassifier()
    OneVsRestClassifier(svm.SVC())


def main(classifier, test_set, output_file, selector=None):
    """
    """

    """
    Input
    """

    LOGGER.info('Reading test set...')
    with open(test_set, 'r') as f:
        (ids, test_features, _, _, _) = get_vector_from(f)

    """
    Feature selection
    """

    if selector:
        features_ranker = joblib.load(selector)
        features_ranker.transform(test_features)

    """
    Predictions
    """

    clf = joblib.load(classifier)

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
    argparser.add_argument('classifier', help='trained classifier (bin file)')
    argparser.add_argument('-s', '--selector', default=None, help='trained features selector (bin file)')
    argparser.add_argument('-i', '--input', default=DEFAULT_TEST_SET, help='input test set')
    argparser.add_argument('-o', '--output', default=DEFAULT_OUTPUT, help='output file')
    args = argparser.parse_args()

    main(args.classifier, args.input, args.output, args.selector)
