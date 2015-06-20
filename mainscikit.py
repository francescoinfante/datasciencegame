from sklearn import svm, cross_validation

from utility.arfftoscikit import get_vector_from


def main():
    with open('./output/output_train.arff', 'r') as f:
        (ids, features, classes) = get_vector_from(f)

    clf = svm.SVC(verbose=2, shrinking=True)
    clf.fit(features, classes)
    cv = cross_validation.cross_val_score(clf, features, classes, cv=1)
    print cv


if __name__ == '__main__':
    main()
