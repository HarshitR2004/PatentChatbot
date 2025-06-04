from django.urls import path
from .views import ChatAPIView, SessionChatsAPIView
from . import views

urlpatterns = [
    path('api/', ChatAPIView.as_view(), name='chat-api'), 
    path('',views.chat_page , name='chat-page'), 
    path('session/<int:session_id>/chats/', SessionChatsAPIView.as_view(), name='session-chats'),
]
