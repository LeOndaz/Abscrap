from typing import Iterable
from functools import cached_property
from collections import ChainMap

from bs4.element import Tag

from scrapit.utils import ExclusiveDict

_excluded_attrs = (
    'class', 'id', 'aria-label', 'prefix',
)


class TagSerializer:
    def __init__(self, tags: Iterable[Tag]):
        self.tags = tags

    @cached_property
    def data(self):
        for tag in self.tags:
            yield ChainMap(ExclusiveDict(tag.attrs).exclude(_excluded_attrs), {
                'text': tag.text.strip()
            })
