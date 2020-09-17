from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings
import asyncio
from core.scrapers import MultiScraper
from channels.generic.http import AsyncHttpConsumer


class AsyncScrapersConsumer(AsyncJsonWebsocketConsumer):
    async def websocket_connect(self, message):
        await self.accept()

    async def receive_json(self, data, **kwargs):
        source = data.pop('source', None)

        await self.scrap(data, source=source or settings.SCRAPIT_SITES_CONF_DIR)

    async def scrap(self, data, source=None):
        multi_scraper = MultiScraper(
            source=source,
            search_text=data['search_text']
        )

        for scraper in asyncio.as_completed(await multi_scraper):
            finished = await scraper
            await self.send_json(finished.result)


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    """ MISSED UP, FOR TESTING PURPOSE ONLY, WILL BE REMOVED.. """
    async def websocket_connect(self, message):
        await self.accept()
        await self.channel_layer.group_add(
            'group_1',
            'channel_1'
        )

    async def websocket_receive(self, message):
        print('recieveveveve')
        await self.close()


