from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import transaction

from .models import *

class CandidateRegisterForm(UserCreationForm):
    firstname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={
                                                             'class': 'form-control',
                                                             }))
    
    profile_bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), required=False)
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    list_of_skills = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    github = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    years_of_experience = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    education = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_candidate = True
        user.first_name = self.cleaned_data.get('firstname')
        user.last_name = self.cleaned_data.get('lastname')
        user.save()
        candidate = Candidate.objects.create(
            user=user,
            profile_bio=self.cleaned_data.get('profile_bio'),
            zip_code=self.cleaned_data.get('zip_code'),
            skills=self.cleaned_data.get('list_of_skills'),
            github=self.cleaned_data.get('github'),
            years_of_experience=self.cleaned_data.get('years_of_experience'),
            education=self.cleaned_data.get('education'),
        )
        return user

class RecruiterRegisterForm(UserCreationForm):
    company = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_recruiter = True
        user.save()
        recruiter = Recruiter.objects.create(
            user=user,
            company=self.cleaned_data.get('company'),
            zip_code=self.cleaned_data.get('zip_code')
        )
        return user
        

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                             'class': 'form-control',
                                                             }))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                 'class': 'form-control',
                                                                 'data-toggle': 'password',
                                                                 'id': 'password',
                                                                 'name': 'password',
                                                                 }))

    class Meta:
        model = User
        fields = ['username', 'password']

