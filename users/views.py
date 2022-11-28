from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView

from .forms import *
from .models import User

# Create your views here.

def home(request):
    return render(request, 'users/home.html')

class LoginView(TemplateView):
    template_name = 'users/login.html'
    form_class = LoginForm

class RegisterView(TemplateView):
    template_name = 'users/register.html'

class CandidateRegisterView(CreateView):
    model = User
    form_class = CandidateRegisterForm
    template_name = 'users/register_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'candidate'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('users-home')

class RecruiterRegisterView(CreateView):
    model = User
    form_class = RecruiterRegisterForm
    template_name = 'users/register_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'recruiter'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('users-home')

class CreatePost(CreateView):
    model = Posts
    fields = ['title', 'position_type', 'location', 'skills', 'description', 'expiration_date', 'status']