from functools import wraps

from lib.repository.Repository import Repository
from lib.utility.ObserverClasses import Observable


# Implementazione del design pattern Singleton tramite Decorator (__init__ viene eseguito a ogni chiamata della classe)
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


class ObservableSingleton(Singleton, type(Observable)):
    def __init__(cls, name, bases, mmbs):
        super(ObservableSingleton, cls).__init__(name, bases, mmbs)

    def __call__(cls, *args, **kw):
        return super(ObservableSingleton, cls).__call__()


class RepositoryMeta(ObservableSingleton, type(Repository)):
    def __init__(cls, name, bases, mmbs):
        super(RepositoryMeta, cls).__init__(name, bases, mmbs)

    def __call__(cls, *args, **kw):
        return super(RepositoryMeta, cls).__call__()
