from django import forms
from .models import GuineaPig
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class GuineaPigForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Save"))

    class Meta:
        model = GuineaPig
        fields = ["name", "price", "image_url"]
        widgets = {
            "price": forms.NumberInput(attrs={"min": "0"}),
        }


class GuineaPigFilterForm(forms.Form):
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "Min Price"}),
    )
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={"placeholder": "Max Price"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.form_class = "row row-cols-sm-auto g-3 align-items-center"
        self.helper.field_class = "col-12"
        self.helper.label_class = "visually-hidden"
        self.helper.add_input(Submit("submit", "Filter"))
        self.helper.form_show_errors = False

    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get("min_price")
        max_price = cleaned_data.get("max_price")

        if min_price is not None and max_price is not None and max_price < min_price:
            raise forms.ValidationError("Max price cannot be less than min price.")

        return cleaned_data
