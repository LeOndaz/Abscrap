import re
import requests
import json
from functools import lru_cache, partial
from django.conf import settings

PRICE_PATTERN = '[0-9.,]+'
NVIDIA_GPU_PATTERN = '(RTX)*(GTX)'
AMD_GPU_PATTERN = '(RX)*(XT)*'

test = "Ex Tax:5,750.00 EGP"


def validate_price(price):
    """
    Validates a string as a price
    """
    p = re.search(PRICE_PATTERN, price).group()
    if "," in p:
        return p.replace(',', '')
    else:
        return p


def get_scrapers_conf():
    """

    """
    return settings.SCRAPERS_CONF


def get_stores_config():
    """
    Load the default config file
    """
    return settings.STORES_CONF


def get_store_config(store_codename, **kwargs):
    """
    Get a config for a specific store
    """
    for config in get_stores_config().get('configs'):
        if config['codename'] == store_codename.upper():
            return config

    raise AttributeError()


def get_headers_config():
    """
    Return headers config from scrapers_conf.json or None
    """
    return get_scrapers_conf().get('headers')


def get_timeout_config():
    """"""
    return get_scrapers_conf().get('timeout')


def get_products_list_from_soup(soup, list_class, product_class):
    """
    Returns a generator that yields each product from the product html list
    """
    yield from soup.find(class_=list_class).find_all(class_=product_class)
