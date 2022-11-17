from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView

from ..models import User
from ..forms import CandidateSignupForm

class CandidateSignUpView(CreateView):
    model = User
    form_class = CandidateSignUpView
    template_name = 

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('')