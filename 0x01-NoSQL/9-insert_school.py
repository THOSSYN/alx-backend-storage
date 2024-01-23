#!/usr/bin/env python3
"""A script that insert a new document"""

def insert_school(mongo_collection, **kwargs):
    """A function that inserts a new document
       in a collection based on keyword argument
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
