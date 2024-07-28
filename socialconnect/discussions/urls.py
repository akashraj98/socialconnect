# from django.urls import path
# from .views import (
#     CreatePostView, GetPostView, UpdatePostView, DeletePostView, LikePostView,
#     UnlikePostView, AddCommentView, GetCommentsView
# )

# urlpatterns = [
#     path('posts/', CreatePostView.as_view(), name='create-post'),
#     path('posts/<int:post_id>/', GetPostView.as_view(), name='get-post'),
#     path('posts/<int:post_id>/update/', UpdatePostView.as_view(), name='update-post'),
#     path('posts/<int:post_id>/delete/', DeletePostView.as_view(), name='delete-post'),
#     path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
#     path('posts/<int:post_id>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
#     path('posts/<int:post_id>/comments/', AddCommentView.as_view(), name='add-comment'),
#     path('posts/<int:post_id>/comments/list/', GetCommentsView.as_view(), name='get-comments'),
# ]
