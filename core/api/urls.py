from django.urls import re_path, path
from core.api.consumers import AsyncScrapersConsumer, NotificationConsumer, SubscribeToNotifications

ws_urlpatterns = [
    re_path(r'ws/data/?$', AsyncScrapersConsumer),
    re_path(r'ws/notifications/?$', NotificationConsumer),
]

http_urlpatterns = [
    path(r'notifications/subscribe/', SubscribeToNotifications)
]
