import functools
import time


def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time of {func.__name__}: {end_time - start_time:.4f} seconds")
        return result

    return wrapper


def start_end_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Started executing '{func.__name__}'")
        result = func(*args, **kwargs)
        print(f"Finished executing '{func.__name__}'")
        return result

    return wrapper


def lock_release_decorator(cls_method):
    @functools.wraps(cls_method)
    def wrapper(*args, **kwargs):
        print(f"Sleeping for 20 seconds in {cls_method.__qualname__}")
        time.sleep(20)
        result = cls_method(*args, **kwargs)
        print(f"Lock released in {cls_method.__qualname__}")
        return result

    return wrapper


def simple_exception_catch_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            raise f"Exception in {func.__name__}: {e}"

    return wrapper
