#!/usr/bin/env python3
"""A script that works with Redis server"""

import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """A helper function for count_calls"""
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs for a function"""

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """A helper function"""
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)

        self._redis.rpush(output_key, str(output))

        return output

    return wrapper


def replay(method: Callable) -> None:
    """Replay and display the history of calls for a particular function"""
    key = method.__qualname__
    input_key = f"{key}:inputs"
    output_key = f"{key}:outputs"

    redis_instance = method.__self__._redis

    call_count = int(redis_instance.get(key) or 0)
    print(f"{key} was called {call_count} times:")

    inputs = redis_instance.lrange(input_key, 0, -1)
    outputs = redis_instance.lrange(output_key, 0, -1)

    for inp, out in zip(inputs, outputs):
        formatted_input = eval(inp.decode("utf-8"))
        print(f"{key}(*{formatted_input}) -> {out.decode('utf-8')}")


class Cache:
    """A class representing a cache using Redis"""

    def __init__(self):
        """Instantiate object with Redis client and flush the database"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, int, bytes, float]) -> str:
        """Store the input data in Redis using a random
           key and return the key
        """
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, int]:
        """Retrieve data from Redis using the key and optionally
           apply conversion function
        """
        ret_val = self._redis.get(key)
        if ret_val is not None and fn is not None:
            return fn(ret_val)
        return ret_val

    def get_str(self, key: str) -> Union[str, None]:
        """Retrieve data from Redis as string"""
        return self.get(key, fn=lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieve data from Redis as integer"""
        return self.get(key, fn=lambda x: int(x.decode("utf-8")))
