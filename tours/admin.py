from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import TourCategory, TourPackage, TourImage, TourItinerary, TourReview


class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 3


class TourItineraryInline(admin.TabularInline):
    model = TourItinerary
    extra = 3


@admin.register(TourCategory)
class TourCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(TourPackage)
class TourPackageAdmin(SummernoteModelAdmin):
    list_display = ('title', 'category', 'destination', 'price', 'duration_days', 'seats_available', 'status', 'is_featured')
    list_filter = ('status', 'is_featured', 'is_popular', 'category', 'transport_type')
    search_fields = ('title', 'destination__title')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status', 'is_featured')
    summernote_fields = ('description', 'transport_details', 'hotel_details', 'food_details')
    inlines = [TourImageInline, TourItineraryInline]
    readonly_fields = ('view_count', 'seats_booked')


@admin.register(TourReview)
class TourReviewAdmin(admin.ModelAdmin):
    list_display = ('tour', 'author', 'rating', 'created_at')
    list_filter = ('rating',)
