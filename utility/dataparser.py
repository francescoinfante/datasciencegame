import logging

import dateutil.parser
import isodate

seconds_in_a_day = 24 * 3600


def array_to_dict(row, array):
    """
    "title","description","published_at","viewCount","likeCount","dislikeCount","favoriteCount",
    "commentCount","duration","dimension","definition","caption","licensedContent","topicIds","relevantTopicIds"
    """
    if len(array) != 15:
        raise Warning('Number of fields of row ' + str(row) + ' is ' + str(len(array)))

    test = array[9].lower()
    if test not in ['3d', '2d']:
        logging.warn('dimension not valid for ' + str(row))

    test = array[10].lower()
    if test not in ['hd', 'sd']:
        logging.warn('definition not valid for ' + str(row))

    test = array[11].lower()
    if test not in ['false', 'true']:
        logging.warn('caption not valid for ' + str(row))

    test = array[12].lower()
    if test not in ['false', 'true']:
        logging.warn('licensedContent not valid for ' + str(row))

    topicIds = set(array[13].split(';')) - {''}
    relevantTopicIds = set(array[14].split(';')) - {''}

    try:
        dict = {
            "title": array[0],
            "description": array[1],
            "published_at": dateutil.parser.parse(array[2]),
            "viewCount": int(array[3]),
            "likeCount": int(array[4]),
            "dislikeCount": int(array[5]),
            "favoriteCount": int(array[6]),
            "commentCount": int(array[7]),
            "duration": isodate.parse_duration(array[8]).days * seconds_in_a_day + isodate.parse_duration(
                array[8]).seconds,
            "dimension": array[9],
            "definition": array[10],
            "caption": array[11].lower() == 'true',
            "licensedContent": array[12].lower() == 'true',
            "topicIds": topicIds,
            "relevantTopicIds": relevantTopicIds,
        }
    except:
        raise Warning('Parse error on row ' + str(row))
    return dict
