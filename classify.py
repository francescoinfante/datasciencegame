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


def do_not_call_it():
    svm.LinearSVC()
    naive_bayes.MultinomialNB()


def main(train_set, test_set, output_file, validate=False, k=5):
    executor_calls = []
    with open('input/classifier.cfg') as f:
        for executer in f:
            executer = executer.rstrip().lstrip()
            if executer and not executer.startswith('#'):
                try:
                    executor_calls.append(compile(executer, '<string>', 'eval'))
                except SyntaxError:
                    logging.error('Syntax error: ' + executer)

    if len(executor_calls) != 1:
        logging.error('Not a single classifier is specified')
        exit()

    print 'Reading training set...'
    with open(train_set, 'r') as f:
        (_, train_features, classes) = get_vector_from(f)

    print 'Reading test set...'
    with open(test_set, 'r') as f:
        (ids, test_features, _) = get_vector_from(f)

    if validate:
        print 'Validating...'
        eval_clf = eval(executor_calls[0])
        cv = cross_validation.cross_val_score(eval_clf, train_features, classes, cv=k)
        print 'Accuracy: %f' % cv.mean()

    print 'Training classifier...'
    clf = eval(executor_calls[0])
    clf.fit(train_features, classes)

    print 'Computing predictions...'
    predictions = zip(ids, clf.predict(test_features))

    print 'Writing results...'
    with open(output_file, 'w') as f:
        f.write('id;video_category_id\n')
        csv_writer = csv.writer(f, delimiter=';')
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
    argparser.add_argument('-v', '--validate', default=False,
                           help='output file (csv)')
    argparser.add_argument('-k', '--k-folds', default=5,
                           help='number of folds in the k-folds cross validation')
    args = argparser.parse_args()

    main(args.train_input, args.test_input, args.output, validate=args.validate, k=args.k_folds)
