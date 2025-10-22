import pytest
from django.contrib.auth.models import User, Group
from django.urls import reverse


@pytest.fixture
def create_user(db):
    user = User.objects.create_user(username="testuser", password="password")
    return user


@pytest.fixture
def create_manager(db):
    manager = User.objects.create_user(username="manager", password="password")
    manager_group = Group.objects.get(name="Manager")
    manager.groups.add(manager_group)
    return manager


@pytest.mark.django_db
def test_signup_view(client):
    url = reverse("signup")
    response = client.get(url)
    assert response.status_code == 200
    assert "registration/signup.html" in [t.name for t in response.templates]
