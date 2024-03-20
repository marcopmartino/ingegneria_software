from functools import wraps

from lib.utility.ObserverClasses import Observable


# Implementazione del design pattern Singleton tramite Decorator (__init__ viene eseguito ogni volta)
def singleton(orig_cls):
    orig_new = orig_cls.__new__
    instance = None

    @wraps(orig_cls.__new__)
    def __new__(cls, *args, **kwargs):
        nonlocal instance
        if instance is None:
            instance = orig_new(cls, *args, **kwargs)
        return instance

    orig_cls.__new__ = __new__
    return orig_cls


# Implementazione del design pattern Singleton tramite Metaclass (__init__ viene eseguito una sola volta)
class Singleton(type):
    def __init__(cls, name, bases, mmbs):
        super(Singleton, cls).__init__(name, bases, mmbs)
        cls._instance = super(Singleton, cls).__call__()

    def __call__(cls, *args, **kw):
        return cls._instance


class ObservableSingleton(type(Observable)):
    def __init__(self, name, bases, mmbs):
        super(ObservableSingleton, self).__init__(name, bases, mmbs)
        self._instance = super(ObservableSingleton, self).__call__()

    def __call__(self, *args, **kw):
        return self._instance
