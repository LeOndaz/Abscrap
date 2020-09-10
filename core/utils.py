import re

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


def get_sites_conf_dir():
    """
    Load the default config file
    """
    return settings.SITES_CONF_DIR


def get_sites_conf():
    pass


def get_site_config(store_codename, **kwargs):
    """
    Get a config for a specific store
    """
