from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, password):
        
        if not username:
            raise ValueError('Users mush have a username')

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_recruiter(self, username, password):

        user = self.create_user(emai, password)
        user.recruiter = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):

        user = self.create_user(username, password)
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    recruiter = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    def get_username(self):
        return self.username
    
    def __str__(self):
        return self.username

    objects = UserManager()