from django.contrib import admin
from django.urls import include, path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='users-home'),
    
    # account management urls
    path('login/', LoginView.as_view(success_url='/'), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/candidate', CandidateRegisterView.as_view(), name='register-candidate'),
    path('register/recruiter', RecruiterRegisterView.as_view(), name='register-recruiter'),
    path('dashboard/', DashboardView, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # post management urls
    path('posts/', include(([
        path('', ListPost.as_view(), name='list-posts'),
        path('create/', CreatePost.as_view(), name='create-post'),
        path('<int:pk>/', DetailPost.as_view(), name='post-detail'),
        path('<int:pk>/update/', UpdatePost.as_view(), name='update-post'),
        path('<int:pk>/delete/', DeletePost.as_view(), name='delete-post'),
        path('<int:pk>/show-interest/', show_interest, name='show-interest'),
        path('<int:pk>/candidates/', InterestedCanidatesList.as_view(), name='interested-candidates')
    ])))

]
