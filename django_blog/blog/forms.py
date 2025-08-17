# blog/forms.py
#from __future__ import annotations
from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment
from taggit.forms import TagWidget


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'title'}))
    post_type = forms.ChoiceField(choices=[('article', 'Article'), ('news', 'News')], initial='article', widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Post Type'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}), required=False)
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))
    class Meta:
        model = Post
        fields = ['title', 'post_type', 'content', 'image', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'tags': TagWidget(),
        }

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label='Comment')
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=254, help_text="Required. Enter a valid email address.")


    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


    def clean_email(self) -> str:
        email = self.cleaned_data.get("email", "").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "image"]