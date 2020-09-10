from celery import shared_task
from scrapit.core import ScraperThread as Scraper


@shared_task
def run_scraper(conf, search_text):
    return Scraper(conf, search_text)