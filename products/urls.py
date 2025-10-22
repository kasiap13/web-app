from django.urls import path
from .views import (
    GuineaPigListView,
    GuineaPigCreateView,
    GuineaPigUpdateView,
    GuineaPigDeleteView,
)

app_name = "products"

urlpatterns = [
    path("", GuineaPigListView.as_view(), name="guinea-pig-list"),
    path("add/", GuineaPigCreateView.as_view(), name="guinea-pig-add"),
    path("edit/<int:pk>/", GuineaPigUpdateView.as_view(), name="guinea-pig-edit"),
    path("delete/<int:pk>/", GuineaPigDeleteView.as_view(), name="guinea-pig-delete"),
]
