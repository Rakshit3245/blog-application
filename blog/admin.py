from django.contrib import admin
from .models import Post, PostImage, Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    search_fields = ('post__title', 'user__username')


admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Comment, CommentAdmin)

