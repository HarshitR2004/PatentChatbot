from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
class userSession(models.Model):
    session_id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    ended_at = models.DateTimeField(blank=True, null=True)  
    # Use settings.AUTH_USER_MODEL instead of direct import
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sessions',
        db_column='user_id'
    )

    class Meta:
        db_table = 'usersession_usersession'

    def __str__(self):
        return f"UserSession(user_id={self.user.userID}, session_id={self.session_id})"
