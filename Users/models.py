from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsersManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username=username, email=email, password=password)
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser):
    userID = models.AutoField(primary_key=True, db_column='userID')
    username = models.CharField(max_length=150, unique=True, db_column='username')
    email = models.EmailField(unique=True, db_column='email')
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    objects = UsersManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    def get_userID(self):
        return self.userID

    
