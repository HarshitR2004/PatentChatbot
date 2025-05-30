from django.db import models

# Create your models here.
class Users(models.Model):
    userID = models.AutoField(primary_key=True, db_column='userID')
    username = models.CharField(max_length=150, unique=True, db_column='username')
    email = models.EmailField(unique=True, db_column='email')
    password = models.CharField(max_length=128, db_column='password')  # Django handles hashing
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')