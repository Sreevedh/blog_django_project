from django import forms
from .models import Author, Post, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UsernameField

class AuthorForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2','profile_picture')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
