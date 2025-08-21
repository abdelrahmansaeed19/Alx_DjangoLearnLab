from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import HomePageView
from .views import  PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostByTagListView
from .views import CommentCreateView, CommentUpdateView, CommentDeleteView, CommentListView, CommentDetailView
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)
#app_name = "blog"


urlpatterns = [
    #path('', views.HomePageView.as_view(), name='home'),
    path('', HomePageView.as_view(), name='home'),
    # path('login/', CustomLoginView.as_view(), name='login'),
    # path('logout/', CustomLogoutView.as_view(next_page='home'), name='logout'),
    # path('register/', views.RegisterView.as_view(), name='register'),
    #path('profile/', views.ProfileDetailView.as_view(), name='profile-detail'),
    #path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile-edit'),
    path('', include(router.urls)),
    # path('posts/', PostListView.as_view(), name='post-list'),
    # path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    # path('post/new/', PostCreateView.as_view(), name='post-create'),
    # path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    # path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    # path('comments/', CommentListView.as_view(), name='comment-list'),
    # path('comment/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    # path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    # path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    # path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    # path('search/', views.search_posts, name='post-search'),
    # path("tags/<slug:tag_slug>/", views.PostListView.as_view(), name='post-by-tag'),
    # path('tag/<slug:tag_slug>/', PostByTagListView.as_view(), name='post-by-tag'),
    # path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]