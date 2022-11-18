from django.contrib import admin
from django.urls import path
from .views import home, RegisterView

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('admin/', admin.site.urls)
]