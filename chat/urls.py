from django.urls import path
from .views import ChatAPIView, SessionChatsAPIView
from django.views.generic import TemplateView

urlpatterns = [
    path('', ChatAPIView.as_view(), name='chat'),
    path('session/<int:session_id>/chats/', SessionChatsAPIView.as_view(), name='session-chats'),
    path('render_chat/', TemplateView.as_view(template_name='chat/chat.html'), name='chat-render'), 
]
 