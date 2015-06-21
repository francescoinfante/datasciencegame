from argparse import ArgumentParser
import csv
import logging
from os.path import join
from os.path import dirname
from sklearn.externals import joblib
from sklearn import cross_validation, svm, naive_bayes
from sklearn import ensemble
from sklearn.cross_validation import train_test_split
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
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


def svm_tuning(X, y, classifier):
    # Split the dataset in two equal parts
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.5, random_state=0)

    # Set the parameters by cross-validation
    tuned_parameters = [{'C': [1e-3, 5e-3, 1e-2, 5e-2, 1e-1, 5e-1, 1]}]

    score = 'f1_score'
    print("# Tuning hyper-parameters for %s" % score)
    print()

    clf = GridSearchCV(classifier, tuned_parameters, cv=5,
                       scoring='%s_weighted' % score)
    clf.fit(X_train, y_train)

    print("Best parameters set found on development set:")
    print()
    print(clf.best_params_)
    print()
    print("Grid scores on development set:")
    print()
    for params, mean_score, scores in clf.grid_scores_:
        print("%0.3f (+/-%0.03f) for %r"
              % (mean_score, scores.std() * 2, params))
    print()

    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = y_test, clf.predict(X_test)
    print(classification_report(y_true, y_pred))
    print()

    return clf.best_params_


# def compute_max(x, maximums, features_types):
#     non_zero_indexes = x.nonzero()
#     for (i, j) in zip(non_zero_indexes[0], non_zero_indexes[1]):
#         if features_types == 'numeric':
#             maximums[j] = max(x[i, j], maximums[j])
#
#
# def normalize(x, maximums, features_types):
#     non_zero_indexes = x.nonzero()
#     for (i, j) in zip(non_zero_indexes[0], non_zero_indexes[1]):
#         if features_types == 'numeric':
#             x[i, j] /= maximums[j]


def do_not_call_it():
    svm.LinearSVC()
    naive_bayes.MultinomialNB()
    naive_bayes.GaussianNB()
    ensemble.RandomForestClassifier()
    OneVsRestClassifier(svm.SVC())


def main(train_set, test_set, output_file, validate=False, k=5, num_of_features=0, tuning=False):
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

    # train_features = train_features.toarray()
    # test_features = test_features.toarray()

    """
    Feature selection
    """

    if num_of_features > 0:
        LOGGER.info('Selecting features...')
        features_ranker = SelectKBest(chi2, k=num_of_features).fit(train_features, classes)
        joblib.dump(features_ranker, DEFAULT_SELECTOR_FILE)
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
        LOGGER.info('Accuracy: %f' % cv.mean())

    """
    Training and tuning
    """
    LOGGER.info('Training classifier...')
    if tuning and 'linearsvc' in executor_calls[0].lower():
        LOGGER.info('Tuning...')
        best_params = svm_tuning(train_features, classes, eval(executor_calls[0]))
        clf = svm.LinearSVC(C=best_params['C'], verbose=2)
    else:
        clf = eval(executor_calls[0])
    clf.fit(train_features, classes)

    joblib.dump(clf, DEFAULT_MODEL_FILE)

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
    argparser.add_argument('-t', '--tuning', action='store_true', default=False,
                           help='find the best parameters (for now only SVM)')
    args = argparser.parse_args()

    main(args.train_input, args.test_input, args.output, validate=args.validate, k=args.k_folds,
         num_of_features=args.num_of_features, tuning=args.tuning)
