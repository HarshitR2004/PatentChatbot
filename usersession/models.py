from django.db import models
from django.utils import timezone
from django.db import models
# Create your models here.
class userSession(models.Model):
    session_id = models.CharField(max_length=255, unique=True,primary_key=True)
    created_at = models.DateTimeField(timezone.now, editable=False)
    ended_at = models.DateTimeField(blank=True)
    chatID = models.ForeignKey() 

    def __str__(self):
        return f"UserSession(user_id={self.user_id}, session_id={self.session_id})"