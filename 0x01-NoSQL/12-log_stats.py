#!/usr/bin/env python3
"""A script that provides some stats about
   Nginx log stored in MongoDB


use log

db.nginx.aggregate({"$project":
    {"$concat": {"$sum": "$logs", " logs"}}
    {"$concat": "Methods:"},
    {"$concat": "    ", method, " "{"GET", ":", " ", {"$sum": "$methods"}}}
    {"$concat": "    ", method, " "{"POST", ":", " ", {"$sum": "$methods"}}}
    {"$concat": "    ", method, " "{"PUT", ":", " ",{"$sum": "$methods"}}}
    {"$concat": "    ", method, " "{"PATCH", ":", " ", {"$sum": "$methods"}}}
    {"$concat": "    ", method, " "{"DELETE", ":", " ", {"$sum": "$methods"}}}
    {"$concat": {"$all": {"methods": "GET", "path": "/status"}, {"$sum": "$GET", " ", "status check"}}})"""
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient()
db = client.logs

# Display the number of documents
total_logs = db.nginx.count_documents({})
print(f"{total_logs} logs")

# Display the number of documents with each method
methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
for method in methods:
    count = db.nginx.count_documents({"method": method})
    print(f"    method {method}: {count}")

# Display the number of documents with method=GET and path=/status
status_check_count = db.nginx.count_documents({"method": "GET", "path": "/status"})
print(f"{status_check_count} status check")
