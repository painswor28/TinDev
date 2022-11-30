from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='users-home'),
    path('accounts/login/', LoginView.as_view(success_url='/'), name='login'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/register/candidate', CandidateRegisterView.as_view(), name='register-candidate'),
    path('accounts/register/recruiter', RecruiterRegisterView.as_view(), name='register-recruiter'),
    path('posts/create', CreatePost.as_view(), name='create-post'),
    path('accounts/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout')
]
