from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings
import asyncio
from core.scrapers import MultiScraper
from scrapit.utils import Site


class AsyncScrapersConsumer(AsyncJsonWebsocketConsumer):
    async def websocket_connect(self, message):
        await self.accept()

    async def receive_json(self, data, **kwargs):
        source = data.pop('source', None)

        if source:
            print('STARTING')
            await self.scrap(data, source=source)
            print('ENDING')
        else:
            await self.scrap(data, source=settings.SCRAPIT_SITES_CONF_DIR)

        await self.close()

    async def scrap(self, data, source=None):
        multi_scraper = MultiScraper(
            source=source,
            search_text=data['search_text']
        )

        for scraper in asyncio.as_completed(await multi_scraper):
            finished = await scraper
            await self.send_json(finished.result)


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    def websocket_connect(self, message):
        self.accept()

    def websocket_receive(self, message):
        print('recieveveveve')
        self.close()


class ChatConsumer(AsyncJsonWebsocketConsumer):
    pass

