import functools

import flask


class cached_property:
    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


def flask_global_cached_object(func):
    attribute_name = '_' + func.__name__

    @functools.wraps(func)
    def wrapper():
        cached_object = getattr(flask.g, attribute_name, None)
        if cached_object is None:
            cached_object = func()
            setattr(flask.g, attribute_name, cached_object)
        return cached_object

    return wrapper
