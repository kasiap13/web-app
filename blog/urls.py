from django.urls import path
from .views import (
    BlogPostListView,
    BlogPostCreateView,
    BlogPostUpdateView,
    BlogPostDeleteView,
    api_blog_post_list,
    BlogPostDetailView,
)

app_name = "blog"

urlpatterns = [
    path("", BlogPostListView.as_view(), name="blog-post-list"),
    path("<int:pk>/", BlogPostDetailView.as_view(), name="blog-post-detail"),
    path("add/", BlogPostCreateView.as_view(), name="blog-post-add"),
    path("edit/<int:pk>/", BlogPostUpdateView.as_view(), name="blog-post-edit"),
    path("delete/<int:pk>/", BlogPostDeleteView.as_view(), name="blog-post-delete"),
    path("api/posts/", api_blog_post_list, name="api-blog-post-list"),
]
