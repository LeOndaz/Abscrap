from .config import ScrapersGlobalConfig
from .core import HTMLGenericScraper, DjangoModelScraper, JSONGenericScraper, HTMLGenericMultiScraper

__all__ = (
    'ScrapersGlobalConfig', 'DjangoModelScraper', 'HTMLGenericMultiScraper',
    'HTMLGenericScraper'
)
