from django.db import models
from django.utils import timezone


class SiteSettings(models.Model):
    owner_name = models.CharField(max_length=100, default='Muhammadali')
    owner_title = models.CharField(max_length=200, default='Software Engineer | Django Developer')
    owner_bio = models.TextField(blank=True)
    owner_avatar = models.ImageField(upload_to='owner/', blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    telegram_url = models.URLField(blank=True)
    telegram_username = models.CharField(max_length=100, blank=True)
    github_url = models.URLField(blank=True)
    github_username = models.CharField(max_length=100, blank=True)
    youtube_url = models.URLField(blank=True)
    youtube_username = models.CharField(max_length=100, blank=True)
    instagram_url = models.URLField(blank=True)
    instagram_username = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    linkedin_username = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=300, blank=True)
    university = models.CharField(max_length=300, blank=True, default="Toshkent Axborot Texnologiyalari Universiteti Samarqand filiali")
    major = models.CharField(max_length=200, blank=True, default="Dasturiy Injiniring")
    skills = models.TextField(blank=True, help_text="Vergul bilan ajrating: Python, Django, FastAPI")

    class Meta:
        verbose_name = 'Sayt Sozlamalari'
        verbose_name_plural = 'Sayt Sozlamalari'

    def __str__(self):
        return "Sayt Sozlamalari"

    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()]


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
