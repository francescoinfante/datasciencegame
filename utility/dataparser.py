def array_to_dict(array):
    """
    "video_category_id","title","description","published_at","viewCount","likeCount","dislikeCount","favoriteCount",
    "commentCount","duration","dimension","definition","caption","licensedContent","topicIds","relevantTopicIds"
    """
    dictionary = dict()
    attribute_list = ["video_category_id","title","description","published_at","viewCount","likeCount","dislikeCount","favoriteCount",
    "commentCount","duration","dimension","definition","caption","licensedContent","topicIds","relevantTopicIds"]

    for i in range(0,15):
        dictionary[attribute_list[i]] = array[i]

    return dictionary
