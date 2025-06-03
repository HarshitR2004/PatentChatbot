from django.db import models
from django.core.validators import FileExtensionValidator

class Documents(models.Model):
    docid = models.AutoField(primary_key=True) 
    patentNumber = models.CharField(max_length=20)
    uploadTime = models.DateTimeField(auto_now_add=True)
    documentPath = models.FileField(
        upload_to='documents/patents/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Only PDF files are allowed"
    )

    def __str__(self):
        return f"{self.patentNumber} - Doc {self.docid}"

