import json
from pathlib import Path
from functools import singledispatch
from collections.abc import Iterable
from functools import cached_property
from collections import ChainMap, UserDict
from collections.abc import Mapping
from typing import Iterable


class ExclusiveDict(UserDict):
    """
    A dict that allows excluding keys
    """

    def exclude(self, excludes: Iterable):
        return self.__class__({
            key: val for key, val in self.items() if key not in excludes
        })


def is_json_serialiszable(obj):
    """
    Check if object is JSON serializable
    """
    try:
        json.dumps(obj)
        return True
    except (TypeError, OverflowError):
        return False


class Site:
    """
    This takes a path to a JSON config file.
    When accessing self.conf, this returns the JSON file as a dict.
    """

    def __init__(self, source):
        path = Path(source).resolve(strict=True)
        fname = path.name

        if fname.startswith('#'):
            raise TypeError

        try:
            # assume file path
            self.conf = json.load(open(path))
        except TypeError:
            # assume dict
            self.conf = source

    def get(self, *args, **kwargs):
        """
        Delegates getting anything from a Site object to it's .conf property (dict)
        """
        return self.conf.get(*args, **kwargs)

    def __repr__(self):
        return self.conf.get('name')

    @classmethod
    def from_iter(cls, iterable):
        """
        Takes an iterable of config files, returns a lazy Site object generator.
        """
        for conf in iterable:
            if not conf.name.startswith('#'):
                yield cls(conf)

    @classmethod
    def from_dir(cls, directory):
        """
        Same as cls.from_iter() but the iterable in this case is the contents of a directory.
        """
        yield from cls.from_iter(directory.iterdir())

    @classmethod
    def from_source(cls, source):
        """
        Utilizes all of the above methods
        """
        try:
            # assume path
            path = Path(source).resolve(strict=True)
            if path.is_dir():
                # assume dir path
                yield from cls.from_dir(path)
                print('#dirpath')
            else:
                # assume file path
                yield cls(source)
                print('#filepath')
        except TypeError:
            # dict has a virtual superclass of iterable so we can't check if it's iterable.
            if not isinstance(source, Mapping):
                # assume non-dict iterable
                yield from cls.from_iter(source)
                print('#fromiterable')
            else:
                # assume dict
                yield cls(source)
                print('#dict')


def get_items_list_from_soup(soup, list_attrs, item_attrs):
    """
    Returns a generator that yields each item from the items html list
    """
    list_soup = soup.select_one(**list_attrs)

    if list_soup is not None:
        yield from list_soup.select(**item_attrs)
