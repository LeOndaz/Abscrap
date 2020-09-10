from .config import ScrapersGlobalConfig
from .core import HTMLGenericScraper, HTMLDjangoScraper, JSONGenericScraper, HTMLGenericMultiScraper

__all__ = (
    'ScrapersGlobalConfig', 'HTMLDjangoScraper', 'HTMLGenericMultiScraper',
    'HTMLGenericScraper'
)
