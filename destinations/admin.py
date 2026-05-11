from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Destination, DestinationImage, DestinationReview


class DestinationImageInline(admin.TabularInline):
    model = DestinationImage
    extra = 3


@admin.register(Destination)
class DestinationAdmin(SummernoteModelAdmin):
    list_display = ('title', 'district', 'difficulty', 'best_season', 'is_featured', 'is_active', 'view_count')
    list_filter = ('difficulty', 'best_season', 'is_featured', 'is_active')
    search_fields = ('title', 'location', 'district')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_featured', 'is_active')
    summernote_fields = ('description', 'weather_info', 'safety_tips')
    inlines = [DestinationImageInline]


@admin.register(DestinationReview)
class DestinationReviewAdmin(admin.ModelAdmin):
    list_display = ('destination', 'author', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('destination__title', 'author__username')
