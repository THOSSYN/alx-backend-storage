#!/usr/bin/env python3
"""A script that returns list of school
   having specific topics
"""

def schools_by_topic(mongo_collection, topic):
    """Python function that returns the list of
       school having a specific topic
    """
    school_list = list(mongo_collection.find({"topics": topic}))
    return school_list
