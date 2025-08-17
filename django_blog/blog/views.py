from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, ListView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm, PostForm
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Post
from django.contrib.auth.decorators import login_required, user_passes_test

class HomePageView(TemplateView):
    template_name = 'blog/base.html'
class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'blog/login.html'
    def get_success_url(self):
        messages.success(self.request, "You have successfully logged in.")
        return reverse_lazy('home')
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return self.render_to_response(self.get_context_data(form=form))

class CustomLogoutView(LogoutView):
    pass

class ProfileDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'blog/profile_detail.html'

class ProfileUpdateView(LoginRequiredMixin, FormView):
    template_name = 'blog/profile_edit.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('profile-detail')

    http_method_names = ['get', 'post']  # <-- contains "method"

    def post(self, request, *args, **kwargs):
        """Handle POST requests to update user profile details."""
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your profile has been updated.")
        return super().form_valid(form)

class RegisterView(FormView):
    template_name = 'blog/register.html'
    form_class = RegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('profile-detail')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        messages.success(self.request, "Registration successful. You can now log in.")
        return super().form_valid(form)
    
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully.")
        return super(PostCreateView, self).form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully.")
        return super(PostUpdateView, self).form_valid(form)
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')




