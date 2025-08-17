from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import HomePageView, CustomLoginView, CustomLogoutView
from .views import  PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

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
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]