from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from django.contrib.auth.views import FormView, LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from decorators import recruiter_required
from .forms import *
from .models import *
from django.urls import reverse_lazy

# Create your views here.

def home(request):
    model = User
    return render(request, 'users/home.html')

class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def form_valid(self, form):
        return super(LoginView, self).form_valid(form)


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

@method_decorator([login_required], name='dispatch')
class ListPost(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'users/list_posts.html'

    def get_queryset(self):
        user = self.request.user

        if user.is_recruiter:
            try:
                queryset = Post.objects.filter(creator=user)
            except Post.DoesNotExist:
                queryset = []

        elif user.is_candidate:
            try:
                queryset = Post.objects.all()
            except Post.DoesNotExist:
                queryset = []

        return queryset


@method_decorator([login_required, recruiter_required], name='dispatch')
class CreatePost(CreateView):
    model = Post
    fields = ['title', 'position_type', 'location', 'skills', 'description', 'expiration_date', 'status']
    template_name = 'users/recruiter/create_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        user = self.request.user
        post.creator = user
        post.company = user.recruiter.company
        post.save()
        return redirect('users-home')

class DetailPost(DetailView):
    model = Post
    template_name = 'users/post_detail.html'

@method_decorator([login_required, recruiter_required], name='dispatch')
class UpdatePost(UpdateView):
    model = Post
    fields = ['title', 'position_type', 'location', 'skills', 'description', 'expiration_date', 'status']
    template_name = 'users/recruiter/update_post.html'
    success_url = reverse_lazy('list-posts')

@method_decorator([login_required, recruiter_required], name='dispatch')
class DeletePost(DeleteView):
    model = Post
    template_name = 'users/recruiter/delete_post.html'
    success_url = reverse_lazy('list-posts')

class InterestedCanidatesList(DetailView):
    model = Post
    template_name = 'users/post_candidates.html'



@login_required
def DashboardView(request):
    model = User
    return render(request, 'users/recruiter/dashboard.html')


def show_interest(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user

    if post.interested_candidates.filter(user=user).exists():
        post.interested_candidates.remove(user.candidate)
        return redirect('/posts/')

    else:
        post.interested_candidates.add(user.candidate)

        return redirect('/posts/')






