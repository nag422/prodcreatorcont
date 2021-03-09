from django.contrib import admin
from .models import BlogProfile, Relationship, Post, Comment, Like
# Register your models here.

@admin.register(BlogProfile)
class BlogProfile(admin.ModelAdmin):
    prepopulated_fields = {'slug':('first_name','last_name',),}
    
admin.site.register(Relationship)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
