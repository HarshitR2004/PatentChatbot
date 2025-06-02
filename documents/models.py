from django.db import models
from django.utils import timezone
class Documents(models.Model):
    docid = models.IntegerField(primary_key = True, unique = True)
    patentNumber = models.CharField(max_length = 20)
    uploadTime = models.DateTimeField(default=timezone.now)
    documentPath = models.CharField(max_length = 300)

