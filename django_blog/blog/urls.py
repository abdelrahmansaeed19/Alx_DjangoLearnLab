from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import HomePageView, CustomLoginView, CustomLogoutView
from .views import  PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
from .views import ProfileDetailView, ProfileUpdateView, RegisterView
from .views import CommentCreateView, CommentUpdateView, CommentDeleteView, CommentListView, CommentDetailView

#app_name = "blog"


urlpatterns = [
    #path('', views.HomePageView.as_view(), name='home'),
    path('', HomePageView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile-edit'),
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('comments/', CommentListView.as_view(), name='comment-list'),
    path('comment/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('post/<int:post_id>/comment/new/', CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    # path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]