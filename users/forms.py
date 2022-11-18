from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


from .models import Candidate

class RegisterForm(UserCreationForm):
    ROLE_CHOICES = [
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter')
    ]

    first_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'First Name',
                                                              'class': 'form-control',
                                                              }))
    last_name = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name',
                                                              'class': 'form-control',
                                                              }))
    username = forms.CharField(max_length=100,
                                required=True,
                                widget=forms.TextInput(attrs={'placeholder': 'Username',
                                                              'class': 'form-control',
                                                              }))

    #role = forms.CharField(required=True, widget=forms.Select(choices=ROLE_CHOICES, attrs={'placeholder': 'Role','class': 'form-control',}))
    
    password1 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    password2 = forms.CharField(max_length=50,
                                required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password',
                                                                  'class': 'form-control',
                                                                  'data-toggle': 'password',
                                                                  'id': 'password',
                                                                  }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']

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

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username']


class UpdateCandidateForm(forms.ModelForm):
    profile_bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    list_of_skills = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    github = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    years_of_experience = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    education = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Candidate
        fields = ['profile_bio', 'zip_code', 'list_of_skills', 'github', 'years_of_experience', 'education']