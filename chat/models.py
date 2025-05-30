from django.db import models
from django.utils import timezone

class Chat(models.Model):
    chatID = models.IntegerField(max_length = 20, primary_key = True, unique = True)
    startTime = models.DateTimeField(default = timezone.now)
    endTime = models.DateTimeField(default = timezone.now)
<<<<<<< HEAD
    queryText = models.TextField()
=======
    queryText = models.CharField(max_length=500)
    responseText = models.CharField(max_length=500)
>>>>>>> 0ee8edd26ea8aaff8b96a03ea8905eac903e4253

