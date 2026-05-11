from django.db import models


class ContactMessage(models.Model):
    STATUS = [('new', 'New'), ('read', 'Read'), ('replied', 'Replied'), ('closed', 'Closed')]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default='new')
    admin_reply = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.subject}'


class OfficeLocation(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    flag_emoji = models.CharField(max_length=10, blank=True, default='🌍')
    is_headquarters = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-is_headquarters', 'country']

    def __str__(self):
        return f'{self.country} — {self.city}'
