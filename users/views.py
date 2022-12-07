from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from django.contrib.auth.views import FormView, LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from decorators import recruiter_required, candidate_required
from rest_framework import generics
from rest_framework import filters
import django_filters
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

class RecruiterPostFilter(django_filters.FilterSet):
    # if greater than or equal to 1, then there are interested candidates
    interest = django_filters.BooleanFilter(name="interested_candidates")
    # search for 'active' or "Active"
    active = (filters.SearchFilter,)
    search_fields = ('=status')
    class Meta:
        model = Post
        fields = ['status', 'interested_candidates']

class CandidatePostFilter(django_filters.FilterSet):
    # filter by location
    #locat

    pass

@method_decorator([login_required], name='dispatch')
class ListPost(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'users/posts/list.html'
    filter_fields = ('status', 'location', 'title', 'description', 'interested_candidates')
    def get_queryset(self):
        user = self.request.user

        if user.is_recruiter:
            try:
                queryset = Post.objects.filter(creator=user)
                filter_class = RecruiterPostFilter
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
    template_name = 'users/posts/create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        user = self.request.user
        post.creator = user
        post.company = user.recruiter.company
        post.save()
        return redirect('users-home')

class CandidateDetail(DetailView):
    model = Candidate
    template_name = 'users/candidate/dashboard.html'

    def get_slug_field(self):

        return 'user__username'

class DetailPost(DetailView):
    model = Post
    template_name = 'users/posts/detail.html'

@method_decorator([login_required, recruiter_required], name='dispatch')
class UpdatePost(UpdateView):
    model = Post
    fields = ['title', 'position_type', 'location', 'skills', 'description', 'expiration_date', 'status']
    template_name = 'users/recruiter/update_post.html'
    success_url = reverse_lazy('list-posts')

@method_decorator([login_required, recruiter_required], name='dispatch')
class DeletePost(DeleteView):
    model = Post
    template_name = 'users/posts/delete.html'
    success_url = reverse_lazy('list-posts')

class InterestedCanidatesList(DetailView):
    model = Post
    template_name = 'users/posts/candidates.html'

@login_required
@candidate_required
def show_interest(request, pk):
    post = Post.objects.get(pk=pk)
    user = request.user

    if post.interested_candidates.filter(user=user).exists():
        post.interested_candidates.remove(user.candidate)
        return redirect('/posts/')

    else:
        post.interested_candidates.add(user.candidate)

        return redirect('/posts/')


@login_required
def DashboardView(request):
    model = User
    return render(request, 'users/dashboard.html')

@method_decorator([login_required], name='dispatch')
class ListOffers(ListView):

    model = Offer
    context_object_name = 'offers'
    template_name = 'users/offer/list.html'

    def get_queryset(self):
        user = self.request.user

        if user.is_candidate:
            queryset = Offer.objects.filter(candidate=user.candidate)

        elif user.is_recruiter:
            queryset = Offer.objects.filter(recruiter=user.recruiter)


        return queryset

@method_decorator([login_required, recruiter_required], name='dispatch')
class CreateOffer(CreateView):
    model = Offer
    fields = ['salary', 'expiration_date']
    template_name = 'users/offer/create.html'

    def form_valid(self, form):
        offer = form.save(commit=False)
        user = self.request.user
        candidate_user = User.objects.get(username=self.kwargs['candidate_pk'])
        candidate = Candidate.objects.get(user=candidate_user)
        post = Post.objects.get(pk=self.kwargs['post_pk'])
        offer.recruiter = user.recruiter
        offer.candidate = candidate
        offer.post = post
        offer.save()

        return redirect('list-posts')
       
    def get_context_data(self, **kwargs):
        context = super(CreateOffer, self).get_context_data(**kwargs)
        context['candidate_pk'] = self.kwargs['candidate_pk']
        context['post_pk'] = self.kwargs['post_pk']
        return context

    def get_success_url(self):
        return reverse('list-posts')

@login_required
@candidate_required
def accept_offer(request, pk):

    if Offer.objects.get(pk=pk).is_expired() is False:
        Offer.objects.filter(pk=pk).update(accepted=True)
    return redirect('/offers/')

@login_required
@candidate_required
def decline_offer(request, pk):
    
    if not Offer.objects.get(pk=pk).is_expired():
        Offer.objects.filter(pk=pk).update(declined=True)
    return redirect('/offers/')


