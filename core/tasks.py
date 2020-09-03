from celery import shared_task
from core.scrapers.scraper import ScraperThread as Scraper


@shared_task
def run_scraper(conf, search_text):
    return Scraper(conf, search_text)