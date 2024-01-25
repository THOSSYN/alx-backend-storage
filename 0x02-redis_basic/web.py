#!/usr/bin/env python3
"""A script for fetching web page"""

import redis
import requests
import time
from typing import Callable
from functools import wraps


red = redis.Redis()


def mycachefunc(method: Callable) -> Callable:
    """A Helper function for caching response"""

    @wraps(method)
    def wrapper(url, *args, **kwargs):
        """A wrapper function"""
        cache_key = f"cache:{url}"
        cache_result = red.get(cache_key)

        if cache_result:
            return cache_result.decode("utf-8")
        else:
            result = method(url, *args, **kwargs)
            red.setex(cache_key, 10, result.encode("utf-8"))
            return result

    return wrapper


@mycachefunc
def get_page(url: str) -> str:
    """A function that requests a page"""
    res = requests.get(url=url)
    key = f"count:{url}"

    n = red.incr(key)

    if res.status_code == 200:
        return str(res.content)
    else:
        return f"Error: {res.status_code}"


if __name__ == "__main__":
    slow_url = "http://slowwly.robertomurray.co.uk"
    page_content = get_page(slow_url)
    print("Page Content:")
    print(page_content)

    cached_page_content = get_page(slow_url)
    print("Cached Page Content:")
    print(cached_page_content)

    time.sleep(11)

    new_cached_page_content = get_page(slow_url)
    print("New Cached Page Content:")
    print(new_cached_page_content)
