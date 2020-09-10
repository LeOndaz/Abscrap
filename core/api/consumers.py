from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings
import asyncio
from core.scrapers import MultiScraper
from scrapit.utils import Site


class AsyncScrapersConsumer(AsyncJsonWebsocketConsumer):
    async def websocket_connect(self, message):
        await self.accept()

    async def receive_json(self, data, **kwargs):
        stores = data.get('stores')
        if stores:
            pass

        multi_scraper = MultiScraper(
            source=settings.SCRAPIT_SITES_CONF_DIR,
            search_text=data['search_text']
        )

        for scraper in asyncio.as_completed(await multi_scraper):
            finished = await scraper

            await self.send_json(finished.result)

        await self.close()


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    def websocket_connect(self, message):
        self.accept()
