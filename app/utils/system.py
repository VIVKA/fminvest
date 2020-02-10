import sys
import pickle
import datetime
from functools import wraps


# Thanks, https://goshippo.com/blog/measure-real-size-any-python-object/
def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


____global_cache = {}
def daycache(method):  # noqa: E302
    @wraps(method)
    def cached(*args, **kw):
        global ____global_cache
        dayToken = datetime.date.today().isoformat()
        if dayToken not in ____global_cache:
            ____global_cache.clear()
            ____global_cache[dayToken] = {}

        token = '{}{}{}'.format(
            str(method.__name__),
            pickle.dumps(args, 1),
            pickle.dumps(kw, 1),
        )
        if token not in ____global_cache[dayToken]:
            ____global_cache[dayToken][token] = method(*args, **kw)

        return ____global_cache[dayToken][token]
    return cached


def daycacheassetmethod(method):
    def cached(*args, **kw):
        global ____global_cache
        dayToken = datetime.date.today().isoformat()
        if dayToken not in ____global_cache:
            ____global_cache[dayToken] = {}

        token = '{}-{}-{}-{}'.format(
            str(args[0].ticker),
            str(method.__name__),
            pickle.dumps(args[1:], 1),
            pickle.dumps(kw, 1),
        )
        if token not in ____global_cache[dayToken]:
            ____global_cache[dayToken][token] = method(*args, **kw)

        return ____global_cache[dayToken][token]
    return cached


def hourcacheassetmethod(method):
    def cached(*args, **kw):
        global ____global_cache
        hourToken = datetime.datetime.now().strftime("%Y-%m-%d %H")
        if hourToken not in ____global_cache:
            ____global_cache[hourToken] = {}

        token = '{}-{}-{}-{}'.format(
            str(args[0].ticker),
            str(method.__name__),
            pickle.dumps(args[1:], 1),
            pickle.dumps(kw, 1),
        )
        if token not in ____global_cache[hourToken]:
            ____global_cache[hourToken][token] = method(*args, **kw)

        return ____global_cache[hourToken][token]
    return cached
