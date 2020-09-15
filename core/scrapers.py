from scrapit.config import ScrapersGlobalConfig
from scrapit.core import HTMLGenericMultiScraper, HTMLGenericScraper


class DjangoHTMLGenericScraper(HTMLGenericScraper):
    """
    Useless, however, just for consistency.
    """
    pass


class MultiScraper(HTMLGenericMultiScraper):
    scraper_class = DjangoHTMLGenericScraper
