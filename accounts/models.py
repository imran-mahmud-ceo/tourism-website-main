from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class CustomUser(AbstractUser):
    """Extended user model with role-based access control."""

    class Role(models.TextChoices):
        SUPER_ADMIN = 'superadmin', 'Admin'
        CUSTOMER = 'customer', 'Customer'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png', blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_role_display()})'

    @property
    def is_admin(self):
        return self.role == self.Role.SUPER_ADMIN or self.is_superuser