import requests
from bs4 import BeautifulSoup
import threading

from django.conf import settings

from core.scrapers.utils import validate_price
from core.models import Product
from core.mixins import JsonConfigurable
from core.scrapers.utils import get_products_list_from_soup, get_headers_config, get_timeout_config
import aiohttp
import asyncio

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


class Scraper:
    def __init__(self, conf, search_text):
        self.search_text = search_text
        self.conf = conf
        self._done = False

        self.data = {
            'products': [],
            'store': None
        }

        print(search_text)

    async def get(self, **kwargs):
        payload, headers, timeout = self.get_payload(), self.get_headers(), self.get_timeout()

        async with aiohttp.ClientSession() as session:
            url = self.conf.get('defaults').get('url')

            async with session.get(url, params=payload, headers=headers) as response:
                response = await response.text()

        page_soup = BeautifulSoup(response, 'lxml')
        css_conf = self.conf.get('defaults').get('css')

        for item in get_products_list_from_soup(
                page_soup,
                css_conf.get('product-list-selector'),
                css_conf.get('product').get('selector')
        ):
            name = self.conf.get('codename') or item.find(class_=css_conf.get('product').get('title')).text,
            price = validate_price(item.find(class_=css_conf.get('product').get('price')).text)
            image_path = item.find('img')['src']

            self.data['store'] = self.conf.get('name')
            self.data['products'].append({
                'name': name,
                'price': price,
                'image_path': image_path,
            })

        self._done = True
        return self

    def get_headers(self):
        return self.conf.get('defaults').get('headers') or get_headers_config()

    def get_timeout(self):
        return self.conf.get('defaults').get('timeout') or get_timeout_config()

    def get_payload(self):
        return {
            'search': self.search_text,
            **self.conf.get('defaults').get('payload'),
        }

    def __await__(self):
        return self.get().__await__()

    def save(self):
        if self._done:
            for item in self.data['products']:
                Product.objects.create(**item)
