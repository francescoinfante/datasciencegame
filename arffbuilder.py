import os
from itertools import count

from progressbar import ProgressBar


def arff_sparse_builder(file_name, relation_name, attributes, data):
    if not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name))
    out = open(file_name, 'w')
    out.write('@RELATION ' + relation_name + '\n')

    code_list, counter = [], count(0)

    out.write('@ATTRIBUTE ' + 'id' + ' ' + attributes['id'] + '\n')  # id first
    code_list.append(('id', counter.next()))

    for f_name, f_type in sorted(attributes.items()):
        if f_name in ['id', 'video_category_id']:
            continue
        out.write('@ATTRIBUTE ' + f_name + ' ' + f_type + '\n')
        code_list.append((f_name, counter.next()))

    out.write('@ATTRIBUTE ' + 'video_category_id' + ' ' + attributes['video_category_id'] + '\n')  # class last
    code_list.append(('video_category_id', counter.next()))

    out.write('@DATA\n')

    progressbar, progressbar_counter = ProgressBar(maxval=len(data)).start(), count(1)

    code_list = dict(code_list)

    for line in data:
        res = []

        for f_name in line:
            if f_name in code_list:
                res.append((code_list[f_name], line[f_name]))

        out.write('{' + ','.join([str(x) + ' ' + str(y) for x, y in res]) + '}\n')

        progressbar.update(progressbar_counter.next())
    progressbar.finish()
