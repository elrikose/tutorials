import random_list
import time
from functools import wraps

def timing_kwargs(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}({}, {}) - {:.6f} sec'.format(func.__name__, args, kwargs, end-start))
        return result
    return wrapper


def timing(func):
    @wraps(func)
    def wrapper(*args):
        start = time.perf_counter()
        result = func(*args)
        end = time.perf_counter()
        print('{} - {:.6f} sec'.format(func.__name__, end-start))
        return result
    return wrapper

@timing
def time_random_list(i):
    return random_list.randomized_list(i)

@timing
def time_sorted_list(list):
    sorted(list)

if __name__ == "__main__":

  for i in range(20,500):
    list = time_random_list(i)
    time_sorted_list(list)
