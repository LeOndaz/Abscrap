from channels.generic.websocket import AsyncJsonWebsocketConsumer
from core.models import Product
from django.conf import settings
from core.scrapers.scraper import Scraper
import asyncio


class AsyncScrapersConsumer(AsyncJsonWebsocketConsumer):
    async def websocket_connect(self, message):
        await self.accept()

    async def websocket_disconnect(self, message):
        pass

    async def receive_json(self, data, **kwargs):
        coros = []
        for store_conf in settings.STORES_CONF.get('configs'):
            coro = Scraper(store_conf, search_text=data['search_text'])
            coros.append(coro.get())

        for coro in asyncio.as_completed(coros):
            scraper = await coro
            await self.send_json(scraper.data)


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    def websocket_connect(self, message):
        self.accept()
