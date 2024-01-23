#!/usr/bin/env python3
"""A script that lists documents of a collection"""

def list_all(mongo_collection):
    """A function that lists all the documents
       of a collection
    """
    docList = list(mongo_collection.find())

    if len(docList) == 0:
        return []
    return docList
