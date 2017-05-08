from functools import singledispatch
from pkgutil import walk_packages
from importlib import import_module


@singledispatch
def process(object):
    '''전처리'''
    raise NotImplementedError()


for module in walk_packages(__path__):
    import_module('%s.%s' % (__package__, module.name))
