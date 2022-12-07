from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from django.contrib.auth.views import FormView, LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from decorators import recruiter_required, candidate_required
from .forms import *
from .models import *
from django.urls import reverse_lazy
import datetime
from django.db.models import Count

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
    template_name = 'users/posts/list.html'

    def get_queryset(self):

        user = self.request.user

        status_val = self.request.GET.get('status', 'All')
        candidate_val = self.request.GET.get('candidates', 'False')
        search = self.request.GET.get('search', 'search')
        location = self.request.GET.get('location', 'location')

        if user.is_recruiter:
            try:
                queryset = Post.objects.filter(creator=user)
                if status_val == 'inactive':
                    queryset = Post.objects.filter(expiration_date__lt=datetime.date.today())

                elif status_val == 'active':
                    queryset = Post.objects.filter(expiration_date__gte=datetime.date.today())

                if candidate_val == 'True':
                    queryset = Post.objects.annotate(num_candidates=Count('interested_candidates')).filter(num_candidates__gte=1)

            except Post.DoesNotExist:
                queryset = []

        elif user.is_candidate:
            try:
                queryset = Post.objects.all()
                if status_val == 'inactive':
                    queryset = Post.objects.filter(expiration_date__lt=datetime.date.today())

                elif status_val == 'active':
                    queryset = Post.objects.filter(expiration_date__gte=datetime.date.today())

                if location != 'location':
                    queryset = Post.objects.filter(location=location)

                if search != 'search':
                    queryset = Post.objects.filter(description__contains=search)

                
            except Post.DoesNotExist:
                queryset = []

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListPost, self).get_context_data(**kwargs)
        context['status'] = self.request.GET.get('status' , 'All')
        context['candidates'] = self.request.GET.get('candidates', 'False')
        context['search'] = self.request.GET.get('search','search')
        context['location'] = self.request.GET.get('location', 'location')

        return context

@method_decorator([login_required, recruiter_required], name='dispatch')
class CreatePost(CreateView):
    model = Post
    fields = ['title', 'position_type', 'location', 'skills', 'description', 'expiration_date']
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


