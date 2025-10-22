from django import forms
from .models import BlogPost
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class BlogPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Save"))

    class Meta:
        model = BlogPost
        fields = ["title", "image_url", "content", "category"]
