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
        if '@relation' in line.lower():
            continue
        if '@attribute' in line.lower():
            num_of_attributes += 1
            continue
        if line.strip() == '':
            continue
        instances.append(line[1:-1])

    shape = (len(instances), num_of_attributes - 2)
    matrix = sps.coo_matrix(shape)

    classes = []
    ids = []
    i = 0
    for instance in instances:
        v = [(j, value) for (j, value) in map(lambda x: x.split(' '), instance.split(','))]
        ids.append(v[0])
        classes.append(v[-1])
        for (j, value) in v[1:-1]:
            matrix[i][j] = int(value)
        i += 1

    return np.array(ids), matrix, np.array(classes)
