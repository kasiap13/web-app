import pytest
from django.urls import reverse
from .models import Category, BlogPost
from users.tests import create_user, create_manager


@pytest.mark.django_db
def test_category_model():
    category = Category.objects.create(name="News")
    assert str(category) == "News"


@pytest.mark.django_db
def test_blog_post_model():
    category = Category.objects.create(name="Tutorials")
    post = BlogPost.objects.create(
        title="How to Care for Your Guinea Pig",
        content="A detailed guide.",
        image_url="http://example.com/guide.jpg",
        category=category,
    )
    assert str(post) == "How to Care for Your Guinea Pig"
    assert post.category.name == "Tutorials"


@pytest.mark.django_db
def test_blog_post_list_view(client):
    url = reverse("blog:blog-post-list")
    response = client.get(url)
    assert response.status_code == 200
    assert "blog/blogpost_list.html" in [t.name for t in response.templates]


@pytest.mark.django_db
def test_blog_post_detail_view(client):
    category = Category.objects.create(name="Testing")
    post = BlogPost.objects.create(
        title="Test Post",
        content="This is the content of the test post.",
        image_url="http://example.com/test.jpg",
        category=category,
    )
    url = reverse("blog:blog-post-detail", kwargs={"pk": post.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert "blog/blogpost_detail.html" in [t.name for t in response.templates]
    assert "Test Post" in str(response.content)
    assert "This is the content of the test post." in str(response.content)
    assert "Testing" in str(response.content)


@pytest.mark.django_db
def test_blog_post_detail_view_not_found(client):
    url = reverse("blog:blog-post-detail", kwargs={"pk": 999})
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_manager_can_access_add_view(client, create_manager):
    client.login(username="manager", password="password")
    url = reverse("blog:blog-post-add")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_normal_user_cannot_access_add_view(client, create_user):
    client.login(username="testuser", password="password")
    url = reverse("blog:blog-post-add")
    response = client.get(url)
    assert response.status_code == 403  # Forbidden


@pytest.mark.django_db
def test_anonymous_user_cannot_access_add_view(client):
    url = reverse("blog:blog-post-add")
    response = client.get(url)
    assert response.status_code == 302  # Redirect to login
