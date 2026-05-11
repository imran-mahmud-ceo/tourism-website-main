from django.db import models
from django.utils.text import slugify
from django.conf import settings


class BlogCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, default='fa-tag')

    class Meta:
        verbose_name_plural = 'Blog Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BlogPost(models.Model):
    STATUS = [('draft', 'Draft'), ('published', 'Published')]
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(BlogCategory, related_name='posts', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='blog_posts', on_delete=models.SET_NULL, null=True)
    featured_image = models.ImageField(upload_to='blogs/')
    excerpt = models.CharField(max_length=400)
    body = models.TextField()
    tags = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='published')
    is_featured = models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['slug']), models.Index(fields=['status', 'is_featured'])]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blogs:detail', kwargs={'slug': self.slug})

    @property
    def read_time(self):
        words = len(self.body.split())
        return max(1, round(words / 200))
