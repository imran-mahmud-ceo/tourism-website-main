"""
Hotels app models: Hotels, rooms, bookings
"""
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from destinations.models import Destination


class Hotel(models.Model):
    STAR_RATING = [(i, f'{i} Star') for i in range(1, 6)]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    destination = models.ForeignKey(Destination, related_name='hotels', on_delete=models.SET_NULL, null=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    featured_image = models.ImageField(upload_to='hotels/')
    address = models.TextField()
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    star_rating = models.PositiveIntegerField(choices=STAR_RATING, default=3)
    has_wifi = models.BooleanField(default=True)
    has_pool = models.BooleanField(default=False)
    has_gym = models.BooleanField(default=False)
    has_restaurant = models.BooleanField(default=True)
    has_parking = models.BooleanField(default=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-star_rating']
        indexes = [models.Index(fields=['slug'])]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('hotels:detail', kwargs={'slug': self.slug})

    def get_min_price(self):
        rooms = self.rooms.filter(is_available=True)
        if rooms.exists():
            return rooms.order_by('price_per_night').first().price_per_night
        return 0


class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotels/gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.hotel.name} — image'


class Room(models.Model):
    ROOM_TYPE = [
        ('standard', 'Standard Room'),
        ('deluxe', 'Deluxe Room'),
        ('couple_suite', 'Couple Suite'),
        ('family_suite', 'Family Suite'),
        ('executive_suite', 'Executive Suite'),
    ]

    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    room_type = models.CharField(max_length=30, choices=ROOM_TYPE, default='standard')
    room_number = models.CharField(max_length=20)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField(default=2)
    has_ac = models.BooleanField(default=True)
    has_wifi = models.BooleanField(default=True)
    has_tv = models.BooleanField(default=True)
    has_balcony = models.BooleanField(default=False)
    breakfast_included = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='rooms/', blank=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ['price_per_night']
        unique_together = ('hotel', 'room_number')

    def __str__(self):
        return f'{self.hotel.name} — {self.get_room_type_display()} ({self.room_number})'
