from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView, FormView

from .forms import *
from .models import *


# Create your views here.

def home(request):
    return render(request, 'users/home.html')


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'users/login.html'


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


class DashboardView(TemplateView):
    if User.is_recruiter:
        template_name = 'users/recruiter.html'
    elif User.is_candidate:
        template_name = 'users/candidate.html'
    else:
        template_name = 'users/dashboard.html'





