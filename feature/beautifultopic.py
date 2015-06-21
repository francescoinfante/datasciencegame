from itertools import count
import logging

from progressbar import ProgressBar

from api import FeatureExtractorI


class BeautifulTopic(FeatureExtractorI):
    def __init__(self):
        self.attributes = dict()
        self.cache = dict()

        progressbar, progressbar_counter = ProgressBar(maxval=221657151).start(), count(1)

        logging.warn('ProgressBar Init BeautifulTopic')

        with open('/home/data-dsg/type.csv', 'r') as f:
            for line in f:
                l = line.split(',')
                mid = l[0][2:]
                type = l[1]
                self.cache[mid] = type
                self.attributes[type] = 'numeric'
                progressbar.update(progressbar_counter.next())

        logging.warn('End ProgressBar Init BeautifulTopic')
        logging.warn('Tot attributes ' + str(len(self.attributes)))

    def extract(self, data):
        topics = data['topicIds'] | data['relevantTopicIds']
        result = {}
        for x in topics:
            if x[2:] in self.cache:
                result[self.cache[x[2:]]] = 1
                print "ok!"
            else:
                print "Missing topic: "+ str(x[2:])

        return result
