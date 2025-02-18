from django.urls import path
from . import views
from .views import (PostListView,
                    PostDetailView,
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView,
                    LikePostView,
                    AboutView
                )

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', PostListView.as_view(), name="blog-list"),
    path("about/", AboutView.as_view(), name="blog-about"),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:post_id>/update-image/', views.post_images, name='image-display'),
    path('post/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:post_id>/comment/', views.post_comment, name='post-comment'),
    path('comment/reply/<int:comment_id>/', views.comment_replay, name='comment-replay'),
    path('add-image/<int:pk>/', views.PostImageCreateView.as_view(), name='add-image'),
    path('delete-image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('search/', views.search_blog, name='search_blog'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# function urls

# path('', views.home,name="blog-home"),
# path('post/<int:pk>/like/', views.like_post, name='like-post'),
# path('about', views.about, name="blog-about"),




