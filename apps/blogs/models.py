from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from apps.users.models import CustomUser
import math


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    preview = models.CharField(max_length=350, blank=True)
    thumbnail = models.ImageField(upload_to='blogs/', blank=True, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blogs')
    tags = models.ManyToManyField(Tag, blank=True)
    reading_time = models.PositiveIntegerField(default=1)
    views_count = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_published', '-created_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            slug = base
            n = 1
            while Blog.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        if not self.preview:
            self.preview = self.content[:300]
        word_count = len(self.content.split())
        self.reading_time = max(1, math.ceil(word_count / 200))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
