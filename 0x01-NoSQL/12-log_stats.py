#!/usr/bin/env python3
"""A script that provides some stats about
   Nginx log stored in MongoDB
"""

from pymongo import MongoClient


if __name__ == '__main__':
    client = MongoClient()
    db = client.logs

    total_logs = db.nginx.count_documents({})
    print(f"{total_logs} logs")

    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = db.nginx.count_documents({"method": method})
        print(f"    method {method}: {count}")

    status_check_count = db.nginx.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")
