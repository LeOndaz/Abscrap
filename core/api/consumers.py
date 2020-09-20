from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings
import asyncio
from core.scrapers import MultiScraper
from channels.generic.http import AsyncHttpConsumer


class AsyncScrapersConsumer(AsyncJsonWebsocketConsumer):
    """
    A scraper that accepts each incoming connection and listens on a WebSocket
    When a JSON data is recieved on the following format
    {
        "search_text": "text_to_search_for",
        "source": config_dict
    }
    """

    async def connect(self):
        """
        You'll probably want to override this if you have conditions for accepting the connection.
        """
        await self.accept()

    async def receive_json(self, data, **kwargs):
        """
        This provides a default source for development. In production, This should be removed.
        The clients should send their configs themselves.
        """
        source = data.pop('source')

        await self.scrap(data, source=source or settings.SCRAPIT_SITES_CONF_DIR)

    async def scrap(self, data, source=None):
        multi_scraper = MultiScraper(
            source=source,
            search_text=data['search_text']
        )

        try:
            for scraper in asyncio.as_completed(await multi_scraper):
                finished = await scraper
                await self.send_json(finished.result)
        except TimeoutError:
            # if timeout error, ignore this specific website
            pass


class SubscribeToNotifications(AsyncHttpConsumer):
    async def http_request(self, message):
        print(message)
        await self.channel_layer.group_send(
            'notifications',
            {
                "type": "handle.notification",
                "text": "NOTIFICATION SUCCESS"
            }
        )
        await self.send_response(status=200, body=b"")


class NotificationConsumer(AsyncJsonWebsocketConsumer):
    """ MISSED UP, FOR TESTING PURPOSE ONLY, WILL BE REMOVED.. """

    async def connect(self):
        await self.channel_layer.group_add(
            'notifications',
            self.channel_name,
        )
        await self.accept()

    async def websocket_receive(self, message):
        print('recieveveveve')
        await self.send_json({'send': '2'})

    async def handle_notification(self, evt):
        await self.send_json({
            'notification': evt['text'],
        })
