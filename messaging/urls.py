from django.urls import path
from .views import ConversationView, UpdateMessageReadStatusAPIView

urlpatterns = [
    path('update_read_status/', UpdateMessageReadStatusAPIView.as_view(), name='update_read_status'),
    path('conversations/<int:user_id_1>/<int:user_id_2>/', ConversationView.as_view(), name='get_conversations'),
]
