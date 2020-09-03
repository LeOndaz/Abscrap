import requests
from bs4 import BeautifulSoup
import threading
from core.scrapers.utils import validate_price
from core.scrapers.websites import SIGMA_COMPUTER
from core.models import Product


class SigmaComputerItem:
    def __init__(self, name, price, image_path):
        self.name = name
        self.price = price
        self.image_path = image_path

    def is_in_db(self):
        if Product.objects.filter(name=self.name, price=self.price, store="SPC").exists():
            return True
        else:
            return False

    def save_to_db(self):
        Product.objects.create(name=self.name, price=self.price, image_path=self.image_path, store="SPC")


class SigmaComputerScraper(threading.Thread):
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
   }

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
            'submit_search': ''
        }
        req = requests.get(SIGMA_COMPUTER, params=payload, timeout=10, headers=SigmaComputerScraper.headers)

        page_soup = BeautifulSoup(req.text, 'lxml')

        for item in page_soup.find_all(class_='product-layout'):
            spc_item = SigmaComputerItem(name=item.find(class_='caption hide-cont').text.strip(),
                                         price=validate_price(item.find(class_='price').text.strip()),
                                         image_path="https://sigma-computer.com/" + item.find(class_="img-2 img-responsive")['src'])

            if spc_item.is_in_db():
                print('###### IS IN DB SIGMA #########')
                continue
            else:
                print('###### NOT IN DB SIGMA #########')
                spc_item.save_to_db()

