from django import forms as forms
import django.forms as formy

from network.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post',
        ]
        widgets = {
            'post': formy.Textarea(attrs={
                "class": "form-control ",
                "id": "control-textarea",
                "placeholder": "Write something here...",
                'name': "post "
            })
        }
