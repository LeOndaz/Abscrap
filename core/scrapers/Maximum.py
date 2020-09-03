import requests
from bs4 import BeautifulSoup
import threading
from core.scrapers.utils import validate_price
from core.scrapers.websites import MAXIMUM
from core.models import Product


class MaximumStoreItem:
    def __init__(self, name, price, image_path):
        self.name = name
        self.price = price
        self.image_path = image_path

    def is_in_db(self):
        if Product.objects.filter(name=self.name, price=self.price, store="MX").exists():
            return True
        else:
            return False

    def save_to_db(self):
        Product.objects.create(name=self.name, price=self.price, image_path=self.image_path, store="MX")


class MaximumStoreScraper(threading.Thread):
    def __init__(self, search_text):
        threading.Thread.__init__(self)
        self.search_text = search_text
        print(search_text)

    def run(self):
        return self.get()

    def get(self):
        payload = {
            'route': 'product/search',
            'search': self.search_text,
        }

        req = requests.get(MAXIMUM, params=payload, timeout=10)
        page_soup = BeautifulSoup(req.text, 'lxml')
        for item in page_soup.find(id='content').find_all(class_='product-layout'):
            mx_item = MaximumStoreItem(
                name=item.find(class_='product-name').text,
                price=validate_price(item.find(class_='price').text.strip()),
                image_path=item.find(class_='img-responsive')['src']
            )

            if mx_item.is_in_db():
                print('###### IS IN DB MAX #########')
                continue
            else:
                print('###### NOT IN DB MAX #########')
                mx_item.save_to_db()