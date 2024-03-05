from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<sender_id>\d+)/(?P<recipient_id>\d+)/$', ChatConsumer.as_asgi()),
]
