"""
Destinations app models: Bangladesh tourism destinations
"""
from django.db import models
from django.utils.text import slugify
from django.conf import settings


class Destination(models.Model):
    DIFFICULTY = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('challenging', 'Challenging'),
    ]
    SEASON = [
        ('year_round', 'Year Round'),
        ('summer', 'Summer (Mar–Jun)'),
        ('monsoon', 'Monsoon (Jul–Oct)'),
        ('winter', 'Winter (Nov–Feb)'),
        ('autumn', 'Autumn (Sep–Nov)'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    description = models.TextField()
    featured_image = models.ImageField(upload_to='destinations/')
    location = models.CharField(max_length=200)
    district = models.CharField(max_length=100, default='Bangladesh')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY, default='easy')
    best_season = models.CharField(max_length=20, choices=SEASON, default='winter')
    min_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    weather_info = models.TextField(blank=True)
    safety_tips = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-view_count']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_featured', 'is_active']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('destinations:detail', kwargs={'slug': self.slug})

    def get_avg_rating(self):
        reviews = self.destination_reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0

    @property
    def budget_range(self):
        return f'৳{int(self.min_budget):,} – ৳{int(self.max_budget):,}'


class DestinationImage(models.Model):
    destination = models.ForeignKey(
        Destination, related_name='gallery_images', on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='destinations/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.destination.title} — image'


class DestinationReview(models.Model):
    destination = models.ForeignKey(
        Destination, related_name='destination_reviews', on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='destination_reviews', on_delete=models.CASCADE
    )
    rating = models.PositiveIntegerField(default=5)
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('destination', 'author')

    def __str__(self):
        return f'{self.author} → {self.destination} ({self.rating}★)'
