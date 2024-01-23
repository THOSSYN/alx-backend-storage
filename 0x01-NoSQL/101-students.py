#!/usr/bin/env python3
""" A script that return all sorted student"""

def top_students(mongo_collection):
    """function that returns all students
       sorted by average score
    """
    pipeline = [
    {
        "$project": {
            "_id": 1,
            "name": 1,
            "averageScore": {
                "$avg": {
                    "$map": {
                        "input": "$topics",
                        "as": "topic",
                        "in": "$$topic.score"
                    }
                }
            }
        }
    },
    {"$sort": {"averageScore": -1}}
    ]
    result = list(mongo_collection.aggregate(pipeline))

    return result
