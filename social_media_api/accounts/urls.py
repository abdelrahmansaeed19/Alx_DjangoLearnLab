from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, ProfileView, LogoutView, UserViewSet, FollowUserView, UnfollowUserView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/<int:pk>/followuser/", FollowUserView.as_view(), name="follow_user"),
    path("users/<int:pk>/unfollowuser/", UnfollowUserView.as_view(), name="unfollow_user"),
    path("", include(router.urls)),
]
