import importlib

from path import Path


def get_folder(name):
    mod = importlib.import_module(name)
    return Path(mod.__path__[0])
