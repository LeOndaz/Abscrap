import requests
from bs4 import BeautifulSoup
import threading
from core.scrapers.websites import HIGH_END
from core.scrapers.utils import validate_price
from core.models import Product


class HighEndItem:
    def __init__(self, name, price, image_path):
        self.name = name
        self.price = price
        self.image_path = image_path

    def is_in_db(self):
        if Product.objects.filter(name=self.name, price=self.price, store="HE").exists():
            return True
        else:
            return False

    def save_to_db(self):
        Product.objects.create(name=self.name, price=self.price, image_path=self.image_path, store="HE")


class HighEndScraper(threading.Thread):

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

        req = requests.get(HIGH_END, params=payload, timeout=10)
        page_soup = BeautifulSoup(req.text, 'lxml')

        for item in page_soup.find_all(class_='product-layout'):
            he_item = HighEndItem(name=item.find(class_='product-name').text,
                                  price=validate_price(item.find(class_='price-box').text.strip()),
                                  image_path=item.find(class_="img-responsive img-default-image")['src'])

            if he_item.is_in_db():
                print('###### IS IN DB High End #########')
                continue
            else:
                print('###### NOT IN DB High end #########')
                he_item.save_to_db()