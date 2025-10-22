from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.mixins import UserPassesTestMixin
from django.template.loader import render_to_string
from .models import BlogPost, Category
from .forms import BlogPostForm


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "blog_posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"


class BlogPostCreateView(UserPassesTestMixin, CreateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"
    success_url = reverse_lazy("blog:blog-post-list")

    def test_func(self):
        return self.request.user.groups.filter(name="Manager").exists()


class BlogPostUpdateView(UserPassesTestMixin, UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blogpost_form.html"
    success_url = reverse_lazy("blog:blog-post-list")

    def test_func(self):
        return self.request.user.groups.filter(name="Manager").exists()


class BlogPostDeleteView(UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blog:blog-post-list")

    def test_func(self):
        return self.request.user.groups.filter(name="Manager").exists()


def api_blog_post_list(request):
    category_id = request.GET.get("category")
    if category_id:
        posts = BlogPost.objects.filter(category_id=category_id)
    else:
        posts = BlogPost.objects.all()

    rendered_posts = []
    for post in posts:
        context = {"post": post, "user": request.user}
        html_card = render_to_string(
            "blog/includes/blogpost_card.html", context, request=request
        )
        rendered_posts.append(html_card)

    return JsonResponse(rendered_posts, safe=False)
