import os
import pickle
from functools import wraps

cache = {}


def cached(func):
    cache.setdefault(func.__name__, {})

    @wraps(func)
    def wraped(*args, **kwargs):
        cache_key = (args[1:], tuple(kwargs.items()))
        if cache_key in cache[func.__name__]:
            return cache[func.__name__][cache_key]
        else:
            ret = func(*args, **kwargs)
            cache[func.__name__][cache_key] = ret
            pickle.dump(cache, open('data/octopus_cache.pkl', 'wb'))
            return ret
    return wraped


if not cache and os.path.isfile('data/octopus_cache.pkl'):
    cache.update(pickle.load(open('data/octopus_cache.pkl', 'rb')))
