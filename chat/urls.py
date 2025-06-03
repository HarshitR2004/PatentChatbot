from django.urls import path
from .views import ChatAPIView, SessionChatsAPIView
from django.views.generic import TemplateView

urlpatterns = [
    path('api/', ChatAPIView.as_view(), name='chat-api'),  # API endpoint
    path('', TemplateView.as_view(template_name='chat/chat.html'), name='chat-page'), 
    path('session/<int:session_id>/chats/', SessionChatsAPIView.as_view(), name='session-chats'),
]
