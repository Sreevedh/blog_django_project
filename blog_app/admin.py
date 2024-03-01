from django.contrib import admin
from .models import Author, User, Post
# Register your models here.
admin.site.register(Author) 
admin.site.register(User)
admin.site.register(Post)