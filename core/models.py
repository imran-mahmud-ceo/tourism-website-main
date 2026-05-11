"""
Core app models: Site settings, FAQ, Testimonials, Events, Gallery
"""
from django.db import models
from django.utils.text import slugify
from django.utils import timezone


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default='Adventure Bangladesh')
    tagline = models.CharField(max_length=200, default='Explore the Beauty of Bangladesh')
    logo = models.ImageField(upload_to='site/', blank=True)
    favicon = models.ImageField(upload_to='site/', blank=True)
    email = models.EmailField(default='tourism@adventurebangladesh.com')
    phone = models.CharField(max_length=30, default='+880 1700-000000')
    address = models.TextField(default='House 12, Road 5, Gulshan 1, Dhaka 1212, Bangladesh')
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    about_text = models.TextField(blank=True)
    footer_text = models.TextField(blank=True, default='Discover the unexplored beauty of Bangladesh with us.')
    hero_video_url = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class FAQ(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='testimonials/', blank=True)
    message = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f'{self.name} — {self.rating}★'


class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image = models.ImageField(upload_to='events/')
    location = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    seats_available = models.PositiveIntegerField(default=50)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_upcoming(self):
        return self.start_date > timezone.now()


class GalleryImage(models.Model):
    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=50, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title or f'Gallery Image {self.pk}'
