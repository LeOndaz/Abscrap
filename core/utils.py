import re

PRICE_PATTERN = '[0-9.,]+'


def validate_price(price):
    """
    Validates a string as a price
    """
    p = re.search(PRICE_PATTERN, price).group()
    if "," in p:
        return p.replace(',', '')
    else:
        return p
