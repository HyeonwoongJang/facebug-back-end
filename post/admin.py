from django.contrib import admin
from post.models import Comment, Post, ConvertResult

admin.site.register(Post)
admin.site.register(ConvertResult)
admin.site.register(Comment)
