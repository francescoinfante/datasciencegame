from argparse import ArgumentParser
import csv
from sklearn import svm, cross_validation
from os.path import join
from os.path import dirname

from utility.arfftoscikit import get_vector_from

DEFAULT_OUTPUT = join(dirname(__file__), 'output/result-scikit.csv')
DEFAULT_TRAIN_SET = join(dirname(__file__), 'output/output_train.arff')
DEFAULT_TEST_SET = join(dirname(__file__), 'output/output_test.arff')


def main(train_set, test_set, output_file, validate=False, k=5):
    with open(train_set, 'r') as f:
        (_, train_features, classes) = get_vector_from(f)

    with open(test_set, 'r') as f:
        (ids, test_features, _) = get_vector_from(f)

    if validate:
        eval_clf = svm.LinearSVC(verbose=2)
        cv = cross_validation.cross_val_score(eval_clf, train_features, classes, cv=k)
        print 'Accuracy: %f' % cv.mean

    clf = svm.LinearSVC(verbose=2)
    clf.fit(train_features, classes)

    predictions = zip(ids, clf.predict(test_features))

    with open(output_file, 'w') as f:
        csv_writer = csv.writer(f)
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
    argparser.add_argument('-c', default=None,
                           help='C parameter of SVM')
    args = argparser.parse_args()

    main(args.train_input, args.test_input, args.output, validate=args.validate, k=args.k_folds, c=args.c)
