from django.urls import path
from . import views

app_name = 'dashboard' # creates a namespace for this app

urlpatterns = [
    path('', views.index, name='index'),
]