from django.db import models
from django.utils import timezone
<<<<<<< HEAD
from Users.models import Users
from chat.models import Chat


=======
from django.db import models
>>>>>>> a2f33f6fe87130ae86aee4dc2a0e2748081876ea
# Create your models here.
class userSession(models.Model):
    session_id = models.CharField(max_length=255, unique=True,primary_key=True)
    created_at = models.DateTimeField(timezone.now, editable=False)
    ended_at = models.DateTimeField(blank=True)
<<<<<<< HEAD
    chats = models.ManyToManyField(Chat, related_name='sessions', blank=True)
    
=======
    chatID = models.ForeignKey() 
>>>>>>> a2f33f6fe87130ae86aee4dc2a0e2748081876ea

    def __str__(self):
        return f"UserSession(user_id={self.user_id}, session_id={self.session_id})"