import requests
from bs4 import BeautifulSoup
import threading
import json

from core.scrapers.websites import BADR_GROUP
from core.scrapers.utils import validate_price
from core.models import Product
from core.scrapers.utils import get_products_list_from_soup, get_store_config


class BadrGroupScraper(threading.Thread):
    def __init__(self, search_text):
        threading.Thread.__init__(self)
        self.search_text = search_text
        print(search_text)

    def run(self):
        self.get()

    def get(self):
        payload = {
            'search': self.search_text,
        }

        req = requests.get(BADR_GROUP, params=payload, headers={
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
        }, timeout=30)

        page_soup = BeautifulSoup(req.text, 'lxml')

        for item in get_products_list_from_soup(
                page_soup,
                'main-products-wrapper',
                'product-layout',
        ):
            product = Product.objects.get_or_create(
                name=item.find(class_='name').text,
                price=validate_price(item.find(class_='price-tax').text),
                store='BG'
                # image_path=item.find(class_='img-responsive img-first')['src'],
            )