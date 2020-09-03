from django.urls import path, re_path
# from core.api.views import StoresHandler
from core.api.consumers import AsyncScrapersConsumer


# urlpatterns = [
#     path('stores/<str:store_name>/', StoresHandler.as_view()),
# ]

ws_urlpatterns = [
    re_path(r'ws/data/$', AsyncScrapersConsumer)
]
