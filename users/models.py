from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_bio = models.TextField(max_length=500)
    zip_code = models.CharField(max_length=20)
    skills = models.CharField(max_length=200)
    github = models.CharField(max_length=50, blank=True)
    years_of_experience = models.IntegerField()
    education = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username
