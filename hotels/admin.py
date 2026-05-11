from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Hotel, HotelImage, Room


class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 3


class RoomInline(admin.TabularInline):
    model = Room
    extra = 2


@admin.register(Hotel)
class HotelAdmin(SummernoteModelAdmin):
    list_display = ('name', 'destination', 'star_rating', 'is_featured', 'is_active')
    list_filter = ('star_rating', 'is_featured', 'is_active', 'has_pool', 'has_gym')
    search_fields = ('name', 'destination__title', 'address')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_featured', 'is_active')
    summernote_fields = ('description',)
    inlines = [HotelImageInline, RoomInline]


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_number', 'room_type', 'price_per_night', 'capacity', 'is_available')
    list_filter = ('room_type', 'is_available', 'has_ac')
    search_fields = ('hotel__name', 'room_number')
    list_editable = ('is_available',)
