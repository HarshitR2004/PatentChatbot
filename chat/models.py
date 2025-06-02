from django.db import models
from django.utils import timezone

class Chat(models.Model):
    chatID = models.IntegerField(primary_key=True, unique=True)
    startTime = models.DateTimeField(default=timezone.now)
    endTime = models.DateTimeField(default=timezone.now)
    queryText = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    responseText = models.TextField(blank=True, null=True)
    session_id = models.ForeignKey('usersession.userSession', on_delete=models.CASCADE, related_name='chats', db_column='session_id', null=True, blank=True)  # allow null for old entries,

    def __str__(self):
        return f"Chat {self.chatID}"

