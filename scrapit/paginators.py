"""
A paginator(data, n) is basically a lazy object that splits a data iterable into smaller iterables of size n.
"""

import math


class BasePaginator:
    """
    A base class for paginator classes, the first page has index 1.
    """
    paginate_by = 20

    def __init__(self, data, paginate_by, **kwargs):
        self.paginate_by = paginate_by or self.paginate_by
        self.data = data

    def get_page(self, n):
        """
        Should return a page.
        """

        raise NotImplementedError

    def has_page(self, n):
        """
        Should check for the existence of page n
        """
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    @property
    def page_count(self):
        """
        Should return the total number of pages.
        """
        raise NotImplementedError

    @property
    def pages(self):
        """
        Should return an iterator that iterates through pages.
        """
        raise NotImplementedError


class BaseLazyPaginator(BasePaginator):
    """
    Efficient paginator, returns only needed pages.
    """

    def __init__(self, data, paginate_by=20, **kwargs):
        super().__init__(data, paginate_by, **kwargs)

    def get_page(self, n):
        """
        Get a page by it's number, if you want to check for the existence of a page, self.page_exists is more efficient
        """
        yield from self.data[(n - 1) * self.paginate_by: ((n - 1) * self.paginate_by) + self.paginate_by]

    def has_page(self, n):
        """
        Check for the first item of a page, for efficient checking.
        """
        try:
            self.data[(n - 1) * self.paginate_by]  # noqa, this is just for disabling linters
            return True
        except KeyError:
            return False

    @property
    def page_count(self):
        """
        Returns the total number of pages.
        """
        return math.ceil(len(self.data) / self.paginate_by)

    @property
    def pages(self):
        """
        Yield each page, one by one.
        """
        _last_index = 0
        for i in range(math.ceil(len(self.data) / self.paginate_by)):
            yield self.data[_last_index: _last_index + self.paginate_by]
            _last_index += self.paginate_by

    def __iter__(self):
        yield from self.pages

    def __getitem__(self, indices):
        """
        Get items as paginator[page, i]
        """
        page, i = indices
        return tuple(self.get_page(page))[i]