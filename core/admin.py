from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import SiteSettings, FAQ, Testimonial, Event, GalleryImage


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'email', 'phone')


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'rating', 'is_featured')
    list_editable = ('is_featured',)
    list_filter = ('rating', 'is_featured')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'start_date', 'seats_available', 'is_featured', 'is_active')
    list_filter = ('is_featured', 'is_active')
    search_fields = ('title', 'location')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured')
    list_filter = ('category', 'is_featured')
