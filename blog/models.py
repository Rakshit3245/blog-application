from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')

    def num_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

class PostImage(models.Model):
    post = models.ForeignKey(Post, related_name="images", on_delete=models.CASCADE)
    post_images = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return f"Image for {self.post.author}"

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})

    def delete(self, *args, **kwargs):
        if self.post_images:
            if os.path.isfile(self.post_images.path):
                os.remove(self.post_images.path)
        super().delete(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post.pk})

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

