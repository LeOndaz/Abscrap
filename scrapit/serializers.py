from typing import Iterable
from functools import cached_property
from collections import ChainMap
from bs4.element import Tag
from .utils import ExclusiveDict


class TagSerializer:
    """
    Serializes the tag, returns a dict of it's attribute excluding useless scraped attributes.
    """

    excluded_attrs = (
        'class', 'id', 'aria-label', 'prefix', 'hidden', 'width', 'viewBox', 'version', 'aria-hidden'
    )

    def __init__(self, tags: Iterable[Tag]):
        self.tags = tags

    @cached_property
    def data(self):
        for tag in self.tags:
            yield ChainMap(ExclusiveDict(tag.attrs).exclude(self.get_excluded_attrs()), {
                'text': tag.text.strip()
            })

    def get_excluded_attrs(self):
        """
        Override, call super(), add more attrs.
        """
        return self.excluded_attrs
