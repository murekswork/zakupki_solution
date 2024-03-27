import functools
import logging
from time import perf_counter


def time_loger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = perf_counter()
        result = func(*args, **kwargs)
        end_time = perf_counter()
        logging.debug(f'{func.__name__} took {end_time - start_time} seconds')
        return result
    return wrapper
