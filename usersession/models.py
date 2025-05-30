from django.db import models
from django.utils import timezone
from Users.models import Users
from chat.models import Chat


# Create your models here.
class userSession(models.Model):
    session_id = models.CharField(max_length=255, unique=True,primary_key=True)
    created_at = models.DateTimeField(timezone.now, editable=False)
    ended_at = models.DateTimeField(blank=True)
    chats = models.ManyToManyField(Chat, related_name='sessions', blank=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sessions', db_column='user_id')
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='user_sessions', db_column='chat_id')
    

    def __str__(self):
        return f"UserSession(user_id={self.user_id}, session_id={self.session_id})"