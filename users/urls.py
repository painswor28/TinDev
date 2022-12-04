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
    path('candidate/<str:slug>', CandidateDetail.as_view(), name='candidate-detail'),
    

    # post management urls
    path('posts/', include(([
        path('', ListPost.as_view(), name='list-posts'),
        path('create/', CreatePost.as_view(), name='create-post'),
        path('<int:pk>/', DetailPost.as_view(), name='post-detail'),
        path('<int:pk>/update/', UpdatePost.as_view(), name='update-post'),
        path('<int:pk>/delete/', DeletePost.as_view(), name='delete-post'),
        path('<int:pk>/show-interest/', show_interest, name='show-interest'),
        path('<int:pk>/candidates/', InterestedCanidatesList.as_view(), name='interested-candidates'),
        path('<int:post_pk>/offer/<str:candidate_pk>', CreateOffer.as_view(), name='make-offer')
    ]))),

    path('offers/', include(([
        path('', ListOffers.as_view(), name='list-offers'),
        path('<int:pk>/accept', accept_offer, name='accept-offer'),
        path('<int:pk>/decline', decline_offer, name='decline-offer')
    ])))

]
