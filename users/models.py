from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class User(AbstractUser):
    is_candidate = models.BooleanField(default=False)
    is_recruiter = models.BooleanField(default=False)


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


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Posts(models.Model):
    creator = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    position_type = models.CharField(choices=[('Full Time', 'FT'), ('Part Time', 'PT')], max_length=10)
    location = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    company = models.CharField(max_length=100)
    expiration_date = models.DateField()
    status = models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=10)
