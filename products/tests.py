import pytest
from django.urls import reverse
from .models import GuineaPig
from .forms import GuineaPigFilterForm
from users.tests import create_user, create_manager


@pytest.mark.django_db
def test_guinea_pig_model():
    pig = GuineaPig.objects.create(
        name="Fluffy", price=25.50, image_url="http://example.com/fluffy.jpg"
    )
    assert str(pig) == "Fluffy"
    assert pig.name == "Fluffy"
    assert pig.price == 25.50


@pytest.mark.django_db
def test_guinea_pig_list_view(client):
    url = reverse("products:guinea-pig-list")
    response = client.get(url)
    assert response.status_code == 200
    assert "products/guineapig_list.html" in [t.name for t in response.templates]
    assert isinstance(response.context["form"], GuineaPigFilterForm)


@pytest.mark.django_db
def test_manager_can_access_add_view(client, create_manager):
    client.login(username="manager", password="password")
    url = reverse("products:guinea-pig-add")
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_normal_user_cannot_access_add_view(client, create_user):
    client.login(username="testuser", password="password")
    url = reverse("products:guinea-pig-add")
    response = client.get(url)
    assert response.status_code == 403  # Forbidden


@pytest.mark.django_db
def test_anonymous_user_cannot_access_add_view(client):
    url = reverse("products:guinea-pig-add")
    response = client.get(url)
    assert response.status_code == 302  # Redirect to login


@pytest.mark.django_db
def test_guinea_pig_list_view_filter_by_price(client):
    GuineaPig.objects.create(
        name="Piggy1", price=10.00, image_url="http://example.com/1.jpg"
    )
    GuineaPig.objects.create(
        name="Piggy2", price=20.00, image_url="http://example.com/2.jpg"
    )
    GuineaPig.objects.create(
        name="Piggy3", price=30.00, image_url="http://example.com/3.jpg"
    )

    url = reverse("products:guinea-pig-list")
    response = client.get(url, {"min_price": 15, "max_price": 25})

    assert response.status_code == 200
    assert len(response.context["guinea_pigs"]) == 1
    assert response.context["guinea_pigs"][0].name == "Piggy2"


@pytest.mark.django_db
def test_guinea_pig_list_view_invalid_price_filter(client):
    GuineaPig.objects.create(
        name="Piggy1", price=10.00, image_url="http://example.com/1.jpg"
    )
    GuineaPig.objects.create(
        name="Piggy2", price=20.00, image_url="http://example.com/2.jpg"
    )

    url = reverse("products:guinea-pig-list")
    response = client.get(url, {"min_price": -5})

    assert response.status_code == 200
    assert len(response.context["guinea_pigs"]) == 2
    form = response.context["form"]
    assert not form.is_valid()
    assert "min_price" in form.errors


@pytest.mark.django_db
def test_guinea_pig_list_view_max_less_than_min(client):
    GuineaPig.objects.create(
        name="Piggy1", price=10.00, image_url="http://example.com/1.jpg"
    )
    GuineaPig.objects.create(
        name="Piggy2", price=20.00, image_url="http://example.com/2.jpg"
    )

    url = reverse("products:guinea-pig-list")
    response = client.get(url, {"min_price": 25, "max_price": 15})

    assert response.status_code == 200
    assert len(response.context["guinea_pigs"]) == 2
    form = response.context["form"]
    assert not form.is_valid()
    assert "__all__" in form.errors
    assert form.errors["__all__"][0] == "Max price cannot be less than min price."
