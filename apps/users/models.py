from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    telegram = models.CharField(max_length=100, blank=True)
    github = models.CharField(max_length=100, blank=True)

    def is_owner(self):
        return self.role == 'owner'

    def is_admin(self):
        return self.role in ['admin', 'owner']

    def is_student(self):
        return self.role in ['student', 'admin', 'owner']

    def __str__(self):
        return f"{self.username} ({self.role})"
