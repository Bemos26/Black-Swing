from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_member = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

class MemberProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='member_profile')
    role = models.CharField(max_length=100, help_text="e.g. Guitarist, Vocalist")
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='team_images/', blank=True, null=True)
    twitter_link = models.URLField(blank=True)
    facebook_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

