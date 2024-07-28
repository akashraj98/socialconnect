from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegisterView, UserLoginView, UserProfileView,
    FollowUserView, UnfollowUserView, SearchUsersView
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('search', SearchUsersView.as_view(), name='search-users'),
    path('<str:user_name>', UserProfileView.as_view(), name='user-profile'),
    path('<str:user_name>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('<str:user_name>/unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
