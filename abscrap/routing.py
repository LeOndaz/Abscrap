from channels.routing import ProtocolTypeRouter, URLRouter
from core.api.urls import ws_urlpatterns


app = ProtocolTypeRouter({
    'websocket': URLRouter(
        ws_urlpatterns
    ),
})

