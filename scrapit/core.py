from functools import cached_property

from .utils import get_items_list_from_soup, Site
from .config import ScrapersGlobalConfig
from .misc import BeautifulSoup
from .serializers import TagSerializer
import httpx
from .utils import done_or_raise


class GenericScraper:
    """
    Base class for all scrapers
    source: a configuration dict
    """
    verbose = False
    log = False
    global_conf_class = None
    paginator_class = None

    def __init__(self, source, **kwargs):
        self.source = source
        self.kwargs = kwargs
        self._done = False

        self.result = {
            'data': [],
            'site_url': None,
            'site_name': None
        }

    async def activate(self, **kwargs):
        raise NotImplementedError

    async def scrap(self, **kwargs):
        """
        Expects _html as kwarg, named _html because there's a library called html
        """
        raise NotImplementedError

    async def get_html(self, **kwargs):
        """
        Must returns the HTML of the page to be scraped.
        """

        kwargs.setdefault('payload', self.payload)
        kwargs.setdefault('headers', self.headers)
        kwargs.setdefault('timeout', self.timeout)
        kwargs.setdefault('page', 1)

        # TODO: maybe catch timeout here?
        async with httpx.AsyncClient(**kwargs) as client:
            url = self.source.get('defaults').get('url')
            response = await client.get(url)
            return response.text

    @cached_property
    def headers(self):
        """
        Return headers from the source config, or return the default headers in self.global_conf_class
        """
        return self.source.get('defaults').get('headers') or self.global_conf_class.get_headers_config()

    @cached_property
    def timeout(self):
        """
        Return timeout from the source config, or return the default timeout in self.global_conf_class
        """
        return self.source.get('defaults').get('timeout') or self.global_conf_class.get_timeout_config()

    @cached_property
    def payload(self):
        """
        Return payload from the source config, or return the default payload in self.global_conf_class
        """
        return {
            **{
                self.source.get('search_param') or 'search': self.kwargs['search_text']
            },
            **self.source.get('defaults').get('payload', {})
        }

    def __await__(self):
        """
        Awaiting the scraper is the same as awaiting it's activate method.
        """
        return self.activate().__await__()

    def __repr__(self):
        """
        A representation for debugging, not useful for now. @TODO
        """
        return 'Scraper(source="{source})"'.format(source=self.source)

    def finalize(self, **kwargs):
        """
        Do something at the end, can be empty.
        The default is to set the site_name, site_url in the response.
        """
        self.result['site_name'] = self.source.get('name')
        self.result['site_url'] = self.source.get('defaults', {}).get('url')

    @done_or_raise
    def paginate_by(self, num, **kwargs):
        """
        Return the data paginated by num.
        """
        paginator = self.get_paginator_class()
        return paginator(self.result['data'], num, **kwargs)

    def get_paginator_class(self):
        """
        Returns the paginator class to use for pagination.
        """
        return self.paginator_class


class GenericMultiScraper(GenericScraper):
    scraper_class = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._coros = []

    async def scrap(self, **kwargs):
        sites = Site.from_source(self.source)

        for site in sites:
            scraper = self.scraper_class(site, search_text=self.kwargs['search_text'])
            self._coros.append(scraper.activate())

    async def activate(self, **kwargs):
        await self.scrap()
        self._done = True
        return self

    def __iter__(self):
        yield from self._coros


class HTMLGenericScraper(GenericScraper):
    """
    An generic HTML scraper.

    source: a config file
    """
    global_conf_class = ScrapersGlobalConfig

    async def activate(self, **kwargs):
        """
        This activates the scraper, returns the scraper itself after it's finished.
        This is not meant to be overridden, this calls most methods, override the one you want.
        """
        _html = await self.get_html()

        await self.scrap(_html=_html)
        self.finalize()
        self._done = True
        return self

    async def scrap(self, **kwargs):
        """
        The scraping logic, scraps the list, sets the self.data, override this if needed.
        """
        page_soup = BeautifulSoup(kwargs.get('_html'), 'lxml')
        css_conf = self.source.get('defaults').get('css')
        fields = css_conf.get('fields')

        for item_soup in get_items_list_from_soup(
                page_soup,
                css_conf.get('item-list'),
                css_conf.get('item')
        ):
            # TODO
            """
            # this is just for studying the response shape 
            [
                "data": [
                    {
                        "title": {"text": "RTX 2060", "price": "7000 EGP" },
                        "price": "7000 EGP",
                    }
                ]
            ]

            """
            item = {}
            # TODO why iterate this for every field? it's the same
            for field_config in fields:
                field = {}
                field_name, field_kwargs, *field_attrs = field_config

                tag_serializer = TagSerializer(item_soup.select(**field_kwargs))

                for tag in tag_serializer.data:
                    if field_attrs:
                        field_attrs = field_attrs[0]
                        field = {**tag}
                    else:
                        return tag

                item[field_name] = field

            self.result['data'].append(item)


class JSONGenericScraper(GenericScraper):
    """
    A response text is JSON anyway.
    """

    async def activate(self, **kwargs):
        _html = await self.get_html()
        self.finalize(_html=_html)
        self._done = True
        return self

    def finalize(self, **kwargs):
        """
        Takes any keyword argument, just for using it here.
        """
        super().finalize()
        self.result['data'] = kwargs['_html']


class DjangoModelScraper(GenericScraper):
    """
    Should save scrapped data to a django model.
    the self.result['data'] items should be an object with the signature of the model.
    """
    model_class = None
    serializer_class = None

    def save(self):
        """
        When scraping is done, save the scrapped data to database, item must match the scraped item
        In other words, inspect.Signature.bind should work between scrapped data and the model initializer.
        """

        if self._done:
            for item in self.result['data']:
                self.get_model_class().objects.create(**item)

    def serialized(self):
        serializer = self.get_serializer_class()
        return serializer(self.result, many=True).data

    def get_model_class(self):
        return self.model_class

    def get_serializer_class(self):
        return self.serializer_class


class HTMLGenericMultiScraper(GenericMultiScraper):
    """
    source: dir or list of config files or list of dicts
    """
    scraper_class = HTMLGenericScraper


class JSONGenericMultiScraper(GenericMultiScraper):
    scraper_class = JSONGenericScraper
