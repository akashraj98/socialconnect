from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegisterView, UserLoginView, UserProfileView,
    FollowUserView, UnfollowUserView
)

urlpatterns = [
    path('/register/', UserRegisterView.as_view(), name='user-register'),
    path('/login/', UserLoginView.as_view(), name='user-login'),
    path('<int:user_id>/', UserProfileView.as_view(), name='user-profile'),
    path('<int:user_id>/follow/', FollowUserView.as_view(), name='follow-user'),
    path('<int:user_id>/unfollow/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]
