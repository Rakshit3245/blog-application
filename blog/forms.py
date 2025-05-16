from .models import PostImage, Comment
from django import forms

class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['post_images']

