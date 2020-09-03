from bs4 import BeautifulSoup
import threading
import requests
from core.scrapers.websites import EGYPT_LAPTOP
from core.scrapers.utils import validate_price
from core.models import Product


class EgyptLaptopItem:
    def __init__(self, name, price, image_path):
        self.name = name
        self.price = price
        self.image_path = image_path

    def is_in_db(self):
        if Product.objects.filter(name=self.name, price=self.price, store="EL").exists():
            return True
        else:
            return False

    def save_to_db(self):
        Product.objects.create(name=self.name, price=self.price, image_path=self.image_path, store="EL")


class EgyptLaptopScraper(threading.Thread):
    def __init__(self, search_text):
        threading.Thread.__init__(self)
        self.search_text = search_text
        self.items = []
        print(search_text)

    def run(self):
        self.get()

    def get(self):
        payload = {
            'search_performed': 'Y',
            'dispatch': 'products.search',
            'q': self.search_text
        }

        req = requests.get(EGYPT_LAPTOP, params=payload, timeout=10)
        page_soup = BeautifulSoup(req.text, 'lxml')

        for item in page_soup.find_all(class_='ut2-gl__body'):
            el_item = EgyptLaptopItem(name=item.find(class_='ut2-gl__name').text.strip(),
                                      price=validate_price(item.find(class_='ut2-gl__price').find(class_='ty-price').text),
                                      image_path="")

            if el_item.is_in_db():
                print('###### IS IN DB EGYPT LAP #########')
                continue
            else:
                print('###### NOT IN DB EGYPT LAP #########')
                el_item.save_to_db()

    @staticmethod
    def get_item_name(item):
        pass

    def save(self):
        pass
