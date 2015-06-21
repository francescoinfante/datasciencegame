from itertools import count

from progressbar import ProgressBar

from bagofwordsofdescription import BagOfWordsOfDescription
from bagofwordsoftitle import BagOfWordsOfTitle
from bagofwordsunited import BagOfWordsUnited
from bagofwordsunitedtfidf import BagOfWordsUnitedTFIDF
from beautifultopic import BeautifulTopic
from containsrelevanttopic import ContainsRelevantTopic
from containstopic import ContainsTopic
from containstopicunited import ContainsTopicUnited
from containstopicunitedtfidf import ContainsTopicUnitedTFIDF
from counterfit import CounterFit
from exactduration import ExactDuration
from hascaption import HasCaption
from is3d import Is3D
from ishd import IsHD
from islicensed import IsLicensed
from language import LangID
from publisheddate import PublishedDate
from publisheddatecyclic import PublishedDateCyclic
from rangeclassify import RangeClassify


def extract_features(plugins, sample):
    result = []

    progressbar, progressbar_counter = ProgressBar(maxval=len(sample)).start(), count(1)

    for s in sample:
        feature_vector = dict([('id', s[0]), ('video_category_id', s[2])])
        for x in plugins:
            prefix = x.__class__.__name__
            feature_vector.update({prefix + ':' + str(feat_name): feat_value
                                   for feat_name, feat_value in x.extract(s[1]).iteritems()})

        result.append(feature_vector)
        progressbar.update(progressbar_counter.next())
    progressbar.finish()

    return result


def get_attributes(plugins, possible_classes):
    attr = dict([('id', 'numeric'), ('video_category_id', '{' + ','.join(possible_classes) + '}')])

    for x in plugins:
        prefix = x.__class__.__name__
        attr.update({prefix + ':' + str(feat_name): feat_value
                     for feat_name, feat_value in x.get_attributes().iteritems()})

    return attr
