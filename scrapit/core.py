from bs4 import BeautifulSoup as OldBeautifulSoup
import asyncio

# from scrapit import validate_price, ScrapersGlobalConfig
from scrapit.config import ScrapersGlobalConfig
from scrapit.utils import get_items_list_from_soup, Site, is_json_serialiszable
from scrapit.serializers import TagSerializer
import httpx
import json

# from contextlib import


class BeautifulSoup(OldBeautifulSoup):
    def __getitem__(self, key):
        if key == 'text':
            return self.text.strip()

        return super().__getitem__(key)


class GenericScraper:
    """
    Base class for all scrapers
    source: a configuration dict
    """
    verbose = False
    log = False
    global_conf_class = None

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

    async def initiate_request(self):
        """
        Must returns the HTML of the page to be scraped.
        """
        payload, headers, timeout = self.get_payload(), self.get_headers(), self.get_timeout()

        # TODO: catch timeout here
        async with httpx.AsyncClient(headers=headers, params=payload, timeout=timeout) as client:
            url = self.source.get('defaults').get('url')
            response = await client.get(url)
            return response.text

    def get_headers(self):
        return self.source.get('defaults').get('headers') or self.global_conf_class.get_headers_config()

    def get_timeout(self):
        return self.source.get('defaults').get('timeout') or self.global_conf_class.get_timeout_config()

    def get_payload(self):
        return {
            **{
                self.source.get('search_param') or 'search': self.kwargs['search_text']
            },
            **self.source.get('defaults').get('payload', {})
        }

    def __await__(self):
        return self.activate().__await__()

    def __repr__(self):
        return 'Scraper(source="{source})"'.format(source=self.source)


class GenericMultiScraper(GenericScraper):
    scraper_class = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._scrapers = []

    async def scrap(self, **kwargs):
        sites = Site.from_source(self.source)

        for site in sites:
            scraper = self.scraper_class(site, search_text=self.kwargs['search_text'])
            self._scrapers.append(scraper.activate())

    async def activate(self, **kwargs):
        await self.scrap()
        self._done = True
        return self

    def __iter__(self):
        yield from self._scrapers


class HTMLGenericScraper(GenericScraper):
    """
    A site scraper.

    source: a config file
    """

    async def activate(self, **kwargs):
        """
        This activates the scraper, returns the scraper itself after it's finished.
        This is not meant to be overridden, this calls most methods, override the one you want.
        """
        response = await self.initiate_request()

        await self.scrap(_html=response)
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

    def finalize(self):
        self.result['site_name'] = self.source.get('name')
        self.result['site_url'] = self.source.get('defaults').get('url')


class JSONGenericScraper(GenericScraper):
    """
    A response text is JSON anyway.
    """

    async def activate(self, **kwargs):
        return await self.initiate_request()

    async def initiate_request(self):
        response = await super().initiate_request()
        return json.loads(response)


class HTMLDjangoScraper(HTMLGenericScraper):
    model_class = None
    serializer_class = None

    def save(self):
        """
        When scraping is done, save the scrapped data to database
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


class HTMLGenericMultiScraper(GenericMultiScraper, HTMLGenericScraper):
    """

    source: dir or list of config files or list of dicts
    """
    scraper_class = HTMLGenericScraper


class JSONGenericMultiScraper(GenericMultiScraper, JSONGenericScraper):
    scraper_class = JSONGenericScraper
