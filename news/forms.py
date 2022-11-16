from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'header',
            'text',
            'categories',
        ]


class DateInput(forms.DateInput):
    input_type = 'date'


class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'

