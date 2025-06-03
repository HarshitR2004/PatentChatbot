from django.db import models

class Documents(models.Model):
    docid = models.AutoField(primary_key = True)
    patentNumber = models.CharField(max_length = 20)
    uploadTime = models.DateTimeField(auto_now=True)
    documentPath = models.CharField(max_length = 300)

    def __str__(self):
        return f"{self.patentNumber}"