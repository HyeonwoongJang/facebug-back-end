from django.urls import path
from post import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list_view'),
    path('<int:user_id>/', views.PostListView.as_view(), name='user_page_view'),
    path('post/image-convert/', views.ImageConvertView.as_view(), name='image_convert_view'),
    path('post/', views.PostView.as_view(), name='post_create_view'),
    path('post/<int:post_id>/', views.PostView.as_view(), name='post_delete_view'),
    path('post/<int:post_id>/like/', views.PostLikeView.as_view(), name='post_like_view'),
    path('post/<int:user_id>/liked_post_view/', views.LikedPostView.as_view(), name='liked_post_view'),
    path('post/<int:post_id>/comment/', views.CommentView.as_view(), name='comment_view'),
    path('post/<int:post_id>/comment/<int:comment_id>/', views.CommentView.as_view(), name='comment_view'),
]