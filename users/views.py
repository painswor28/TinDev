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

# view for user homepage
def home(request):
    # use User model
    model = User
    return render(request, 'users/home.html')

# view for user login page
class LoginView(LoginView):
    # use LoginForm as form class
    form_class = LoginForm
    # call from login template
    template_name = 'users/login.html'
    # executes login function 
    def form_valid(self, form):
        return super(LoginView, self).form_valid(form)

# view for registering user account
class RegisterView(TemplateView):
    template_name = 'users/register.html'

# view specific to candidate registration
class CandidateRegisterView(CreateView):
    # overall model is still User
    model = User
    # but form_class specifies candidate
    form_class = CandidateRegisterForm
    # use users register form template 
    template_name = 'users/register_form.html'
    # specify the context data is specific to candidate and not recruiter
    def get_context_data(self, **kwargs):
        # method is used to populate dictionary object for template context
        kwargs['user_type'] = 'Candidate'
        return super().get_context_data(**kwargs)
    # save user form 
    def form_valid(self, form):
        # save form
        user = form.save()
        # perform login
        login(self.request, user)
        # redirect to the user's homepage upon succesful login
        return redirect('users-home')

# view specific to recruter registration
class RecruiterRegisterView(CreateView):
    # again, overall model is still User
    model = User
    # here, specify we're registering a Recruiter
    form_class = RecruiterRegisterForm
    # specify template (same as candidate template)
    template_name = 'users/register_form.html'
    # populate dict for template variables
    def get_context_data(self, **kwargs):
        # set user type to recruter, specifying that is the type
        kwargs['user_type'] = 'Recruiter'
        # return and populate object
        return super().get_context_data(**kwargs)
    # save form 
    def form_valid(self, form):
        # save
        user = form.save()
        # perform login 
        login(self.request, user)
        # redirect to home
        return redirect('users-home')

# list all posts - must be logged in to view - if not, go back to dispatch
@method_decorator([login_required], name='dispatch')
class ListPost(ListView):
    # use Post model
    model = Post
    # specify the object we're using the template (posts) - lets us do 'for post in posts'
    context_object_name = 'posts'
    # using the posts template
    template_name = 'users/posts/list.html'
    def get_queryset(self):

        user = self.request.user

        status_val = self.request.GET.get('status', 'All')
        candidate_val = self.request.GET.get('candidates', 'False')
        search = self.request.GET.get('search', '')
        location = self.request.GET.get('location', 'all')

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

                if location != 'all':
                    queryset = Post.objects.filter(location__contains=location)

                if search:
                    queryset = Post.objects.filter(description__contains=search)
                
            except Post.DoesNotExist:
                queryset = []

        return queryset

    def get_context_data(self, **kwargs):
        context = super(ListPost, self).get_context_data(**kwargs)
        context['status'] = self.request.GET.get('status', 'All')
        context['candidates'] = self.request.GET.get('candidates', 'False')
        context['search'] = self.request.GET.get('search', '')
        context['location'] = self.request.GET.get('location', 'all')

        return context

# view for creating post - login is required and you must be a recruiter to create - else, go to dispatch
@method_decorator([login_required, recruiter_required], name='dispatch')
class CreatePost(CreateView):
    # model is Post
    model = Post
    
    # fields of importance listed
    fields = ['title', 'position_type', 'location', 'skills', 'description', 'expiration_date']

    # using posts/create template
    template_name = 'users/posts/create.html'
    # determine validity of form 
    def form_valid(self, form):
        # save form and set commit to false in order to get model object in return
        post = form.save(commit=False)
        # specify user of this request
        user = self.request.user
        # set attributes of post with the user creating it and the company they work for
        post.creator = user
        post.company = user.recruiter.company
        # save that post
        post.save()
        # send back to user homepage
        return redirect('users-home')
# view for candidate's dashboard
class CandidateDetail(DetailView):
    #specify candidate as desired model
    model = Candidate
    # template we're using is the candidate dashboard
    template_name = 'users/candidate/dashboard.html'
    # return name of slug field to be used by lookup slug
    def get_slug_field(self):
        # in this case, the slug is the user username
        return 'user__username'
# view for post's details
class DetailPost(DetailView):
    # set model to post 
    model = Post
    # specify template
    template_name = 'users/posts/detail.html'

# for updating a post - again authentication required - must be logged in and a recruiter, else go to dispatch page
@method_decorator([login_required, recruiter_required], name='dispatch')
class UpdatePost(UpdateView):
    # model is Post
    model = Post
    # fields listed below
    fields = ['title', 'position_type', 'location', 'skills', 'description', 'expiration_date']
    template_name = 'users/posts/update.html'
    # for HTTP redirects and the accessing of url details from urls.py
    success_url = reverse_lazy('list-posts')

# for deleting post - credentials again required and must be recruiter, else go to dispatch page
@method_decorator([login_required, recruiter_required], name='dispatch')
class DeletePost(DeleteView):
    # model is Post
    model = Post
    # use delete template
    template_name = 'users/posts/delete.html'
    # reverse lazy again for urls purposes
    success_url = reverse_lazy('list-posts')

# detailview class for list of interested candidates
class InterestedCanidatesList(DetailView):
    # post model and candidates template
    model = Post
    template_name = 'users/posts/candidates.html'

# to shwo interest in a posting - must be logged in and a candidate
@login_required
@candidate_required
def show_interest(request, pk):
    # retrieve specific post's primary key
    post = Post.objects.get(pk=pk)
    # specify user (the user making request)
    user = request.user
    # if already interested and button clicked, remove user from interested list (and redirect to posts)
    if post.interested_candidates.filter(user=user).exists():
        post.interested_candidates.remove(user.candidate)
        return redirect('/posts/')

    else:
        # otherwise add to the interested list
        post.interested_candidates.add(user.candidate)
        # redirect to posts
        return redirect('/posts/')

# to view dashboard, must be logged in
@login_required
def DashboardView(request):
    # uses User model
    model = User
    # go to dashboard template
    return render(request, 'users/dashboard.html')

# listing offers requires user to be logged in, else send to dispatch
@method_decorator([login_required], name='dispatch')
class ListOffers(ListView):
    # specified model is offer
    model = Offer
    # specify the object we're using for the template (offers) - lets us do 'for offer in offers'
    context_object_name = 'offers'
    # offer list template
    template_name = 'users/offer/list.html'
    def get_queryset(self):
        # specify user for this request
        user = self.request.user
        # case when user is a candidate
        if user.is_candidate:
            # filter the queryset to find that specific candidate
            queryset = Offer.objects.filter(candidate=user.candidate)
        # case when user is a recruiter
        elif user.is_recruiter:
            # filter the queryset to find that specific recruiter
            queryset = Offer.objects.filter(recruiter=user.recruiter)

        # return the queryset
        return queryset
# to create an offer, the user must be logged in and a recruiter
@method_decorator([login_required, recruiter_required], name='dispatch')
class CreateOffer(CreateView):
    # using model offer
    model = Offer
    # fields of interest are salary and expiration date
    fields = ['salary', 'expiration_date']
    # using the offer create template
    template_name = 'users/offer/create.html'
    # to save and validate form
    def form_valid(self, form):
        offer = form.save(commit=False)
        # specify user
        user = self.request.user
        # find candidate from candidate_pk
        candidate_user = User.objects.get(username=self.kwargs['candidate_pk'])
        # get the candidate using specific candidate_user 
        candidate = Candidate.objects.get(user=candidate_user)
        # repeat the same post retrieval with post_pk
        post = Post.objects.get(pk=self.kwargs['post_pk'])
        # specify recruiter and candidate 
        offer.recruiter = user.recruiter
        offer.candidate = candidate
        # specify post
        offer.post = post
        # save offer
        offer.save()
        # redirect to list of posts
        return redirect('list-posts')
    # fill dict object for template to call from
    def get_context_data(self, **kwargs):
        context = super(CreateOffer, self).get_context_data(**kwargs)
        # context candidate's pk comes from candidate_pk specified in the kwarg
        context['candidate_pk'] = self.kwargs['candidate_pk']
        # context post's pk comes from post_pk specified in the kwarg
        context['post_pk'] = self.kwargs['post_pk']
        # return the context's data
        return context
    # successful url can be found with reverse method called on list-posts redirect path
    def get_success_url(self):
        return reverse('list-posts')

# to accept an offer, you must be logged in and a candidate
@login_required
@candidate_required
def accept_offer(request, pk):
    # check first if the offer has expired - if it has, redirect to offers, else update to accepted then redirect to offers
    if Offer.objects.get(pk=pk).is_expired() is False:
        Offer.objects.filter(pk=pk).update(accepted=True)
    return redirect('/offers/')
# to decline an offer, you must also be logged in and a candidate
@login_required
@candidate_required
def decline_offer(request, pk):
    # if offer is not expired, it can be updated to 'declined'; either way, it redirects to offers
    if not Offer.objects.get(pk=pk).is_expired():
        Offer.objects.filter(pk=pk).update(declined=True)
    return redirect('/offers/')


