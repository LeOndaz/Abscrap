from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from core.api.urls import ws_urlpatterns


app = ProtocolTypeRouter({
    'websocket': URLRouter(
        ws_urlpatterns
    )
})