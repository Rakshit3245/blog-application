from .models import PostImage, Comment
from django import forms

class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['post_images']



# class CommentForm(forms.ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['comments', 'parent_comment']
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['parent_comment'].queryset = Comment.objects.filter(parent_comment=None)
