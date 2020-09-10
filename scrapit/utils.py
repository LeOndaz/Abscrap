import json
from pathlib import Path
from functools import singledispatch
from collections.abc import Iterable
from functools import cached_property
from collections import ChainMap, UserDict
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

    def __init__(self, path):
        self.path = path

    @cached_property
    def conf(self):
        """
        Returns a dict from the path provided.
        This property is cached per instance, this means updating a config file needs a server restart.
        """
        return json.load(
            open(Path(self.path).resolve(strict=True))
        )

    def get(self, *args, **kwargs):
        """
        Delegates getting anything from a Site object to it's .conf property (dict)
        """
        return self.conf.get(*args, **kwargs)

    def __repr__(self):
        return self.conf.get('name')

    @classmethod
    def from_iter(cls, source):
        """
        Takes an iterable of config files, returns a lazy Site object generator.
        """
        for conf in source:
            yield cls(conf)

    @classmethod
    def from_dir(cls, source):
        """
        Depends on self.from_iter() and the iterable in this case is the contents of a directory.
        """
        path = Path(source).resolve(strict=True)
        yield from cls.from_iter(path.iterdir())


def get_items_list_from_soup(soup, list_attrs, item_attrs):
    """
    Returns a generator that yields each item from the items html list
    """
    yield from soup.select_one(**list_attrs).select(**item_attrs)
