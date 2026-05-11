"""
Tours app models: Tour packages, categories, itineraries
"""
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from destinations.models import Destination


class TourCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, default='fa-map-marked-alt')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='tour_categories/', blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Tour Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class TourPackage(models.Model):
    STATUS = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('sold_out', 'Sold Out'),
        ('archived', 'Archived'),
    ]
    TRANSPORT = [
        ('bus', 'Bus'),
        ('train', 'Train'),
        ('flight', 'Flight'),
        ('boat', 'Boat'),
        ('private_car', 'Private Car'),
        ('mixed', 'Mixed Transport'),
    ]

    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(TourCategory, related_name='packages', on_delete=models.SET_NULL, null=True)
    destination = models.ForeignKey(Destination, related_name='tour_packages', on_delete=models.SET_NULL, null=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    duration_days = models.PositiveIntegerField(default=3)
    duration_nights = models.PositiveIntegerField(default=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    transport_type = models.CharField(max_length=20, choices=TRANSPORT, default='bus')
    transport_details = models.TextField(blank=True)
    hotel_name = models.CharField(max_length=200, blank=True)
    hotel_details = models.TextField(blank=True)
    included_services = models.TextField(blank=True, help_text='One item per line')
    excluded_services = models.TextField(blank=True, help_text='One item per line')
    food_details = models.TextField(blank=True)
    guide_available = models.BooleanField(default=True)
    seats_total = models.PositiveIntegerField(default=30)
    seats_booked = models.PositiveIntegerField(default=0)
    featured_image = models.ImageField(upload_to='tours/')
    video_url = models.URLField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='active')
    is_featured = models.BooleanField(default=False)
    is_popular = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='created_tours',
        on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-is_popular', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status', 'is_featured']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('tours:detail', kwargs={'slug': self.slug})

    @property
    def effective_price(self):
        return self.discount_price if self.discount_price else self.price

    @property
    def discount_percent(self):
        if self.discount_price and self.price > self.discount_price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0

    @property
    def seats_available(self):
        return max(0, self.seats_total - self.seats_booked)

    @property
    def included_list(self):
        return [s.strip() for s in self.included_services.splitlines() if s.strip()]

    @property
    def excluded_list(self):
        return [s.strip() for s in self.excluded_services.splitlines() if s.strip()]

    def get_avg_rating(self):
        reviews = self.tour_reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0


class TourImage(models.Model):
    tour = models.ForeignKey(TourPackage, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tours/gallery/')
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.tour.title} — image'


class TourItinerary(models.Model):
    tour = models.ForeignKey(TourPackage, related_name='itinerary', on_delete=models.CASCADE)
    day = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        ordering = ['day']
        unique_together = ('tour', 'day')

    def __str__(self):
        return f'Day {self.day}: {self.title}'


class TourReview(models.Model):
    tour = models.ForeignKey(TourPackage, related_name='tour_reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='tour_reviews', on_delete=models.CASCADE
    )
    rating = models.PositiveIntegerField(default=5)
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('tour', 'author')

    def __str__(self):
        return f'{self.author} → {self.tour} ({self.rating}★)'
