from django.contrib import admin
from post.models import Comment, Post, Image

admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Comment)