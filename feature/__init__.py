from itertools import count

from progressbar import ProgressBar

from examplefeature import ExampleFeature

def extract_features(plugins, sample):
    result = []

    progressbar, progressbar_counter = ProgressBar(maxval=len(sample)).start(), count(1)

    for s in sample:
        feature_vector = dict([('id', s[0]), ('class', s[2])])
        for x in plugins:
            prefix = x.__class__.__name__
            feature_vector.update({prefix + ':' + str(feat_name): feat_value
                                   for feat_name, feat_value in x.extract(s[1]).iteritems()})

        result.append(feature_vector)
        progressbar.update(progressbar_counter.next())
    progressbar.finish()

    return result


def get_attributes(plugins, possible_classes):
    attr = dict([('id', 'numeric'), ('class', '{' + ','.join(possible_classes) + '}')])

    for x in plugins:
        prefix = x.__class__.__name__
        attr.update({prefix + ':' + str(feat_name): feat_value
                     for feat_name, feat_value in x.get_attributes().iteritems()})

    return attr
