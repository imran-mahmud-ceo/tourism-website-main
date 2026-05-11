from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import BlogCategory, BlogPost


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'is_featured', 'view_count', 'created_at')
    list_filter = ('status', 'is_featured', 'category')
    search_fields = ('title', 'author__username', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status', 'is_featured')
    summernote_fields = ('body',)
