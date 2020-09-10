from scrapit.config import ScrapersGlobalConfig
from scrapit.core import HTMLGenericMultiScraper, HTMLGenericScraper
from django.conf import settings
import json


class DjangoScrapersGlobalConfig(ScrapersGlobalConfig):
    @classmethod
    def get_global_conf(cls):
        return json.load(open(settings.SCRAPIT_GLOBAL_CONF_DIR))


class DjangoHTMLGenericScraper(HTMLGenericScraper):
    global_conf_class = DjangoScrapersGlobalConfig


class MultiScraper(HTMLGenericMultiScraper):
    global_conf_class = DjangoScrapersGlobalConfig
    scraper_class = DjangoHTMLGenericScraper
