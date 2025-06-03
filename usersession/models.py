from django.db import models
from django.utils import timezone
from Users.models import Users

# Create your models here.
class userSession(models.Model):
    session_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)  # Fix: use default=
    ended_at = models.DateTimeField(blank=True, null=True)  # Add null=True
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sessions', db_column='user_id')


    def __str__(self):
        return f"UserSession(user_id={self.user_id}, session_id={self.session_id})"
