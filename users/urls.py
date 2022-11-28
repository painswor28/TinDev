from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='users-home'),
    path('accounts/login/', RegisterView.as_view() ,name='login'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/register/candidate', CandidateRegisterView.as_view(), name='register-candidate'),
    path('accounts/register/recruiter', RecruiterRegisterView.as_view(), name='register-recruiter')
]