"""Decorators: functions that wrap other functions to add behaviour."""
import time
from functools import wraps

TIMING_LOG = []   # (function_name, seconds) for every timed call


def timer(func):
    """Decorator: time each call, print '[timer] <name> took <x.xxxx> seconds',
    append (name, seconds) to TIMING_LOG, and return the original result.

    The decorated function must keep its own __name__ and __doc__ (use @wraps).
    """
    # TODO: define an inner `wrapper(*args, **kwargs)` decorated with @wraps(func).
    #   Inside: note time.perf_counter() before, call func(*args, **kwargs) and KEEP the result,
    #   note the time after, append (func.__name__, elapsed) to TIMING_LOG, print the line,
    #   and `return result`. Finally `return wrapper` from timer.
    # Until you do this, timer returns func unchanged, so the checks will tell you nothing was timed.
    return func
