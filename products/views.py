from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import GuineaPig
from .forms import GuineaPigForm, GuineaPigFilterForm


class GuineaPigListView(ListView):
    model = GuineaPig
    template_name = "products/guineapig_list.html"
    context_object_name = "guinea_pigs"

    def get_queryset(self):
        queryset = super().get_queryset()
        form = GuineaPigFilterForm(self.request.GET)

        if form.is_valid():
            min_price = form.cleaned_data.get("min_price")
            max_price = form.cleaned_data.get("max_price")

            if min_price is not None:
                queryset = queryset.filter(price__gte=min_price)
            if max_price is not None:
                queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = GuineaPigFilterForm(self.request.GET)
        return context


class GuineaPigCreateView(UserPassesTestMixin, CreateView):
    model = GuineaPig
    form_class = GuineaPigForm
    template_name = "products/guineapig_form.html"
    success_url = reverse_lazy("products:guinea-pig-list")

    def test_func(self):
        return self.request.user.groups.filter(name="Manager").exists()


class GuineaPigUpdateView(UserPassesTestMixin, UpdateView):
    model = GuineaPig
    form_class = GuineaPigForm
    template_name = "products/guineapig_form.html"
    success_url = reverse_lazy("products:guinea-pig-list")

    def test_func(self):
        return self.request.user.groups.filter(name="Manager").exists()


class GuineaPigDeleteView(UserPassesTestMixin, DeleteView):
    model = GuineaPig
    template_name = "products/guineapig_confirm_delete.html"
    success_url = reverse_lazy("products:guinea-pig-list")

    def test_func(self):
        return self.request.user.groups.filter(name="Manager").exists()
