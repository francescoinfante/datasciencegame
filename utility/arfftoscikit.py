import scipy.sparse as sps
import numpy as np


def get_vector_from(arff_file_stream):
    """
    Represents an ARFF dataset in a format suitable for Sci-kit's classifiers.

    :param arff_file_stream: stream of an arff file strctured as <id, feature_1, ..., feature_n, class>
    :return: a triple (ids_vector, sparse_features, classes_vector) where the components are corresponding
    """
    num_of_attributes = 0
    instances = []
    for line in arff_file_stream:
        line = line.strip().lower()
        if line == '' or '@data' in line or '@relation' in line:
            continue
        if '@attribute' in line:
            num_of_attributes += 1
            continue
        instances.append(line[1:-1])

    shape = (len(instances), num_of_attributes - 2)
    matrix = sps.dok_matrix(shape)

    classes = []
    ids = []
    i = 0
    for instance in instances:
        v = [(int(j) - 1, value) for (j, value) in map(lambda x: x.split(' '), instance.split(','))]
        ids.append(int(v[0][1]))
        cur_class = v[-1][1]
        classes.append(int(cur_class))
        for (j, value) in v[1:-1]:
            matrix[(i, j)] = int(value)
        i += 1

    return np.array(ids), matrix, np.array(classes)
