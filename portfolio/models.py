from django.db import models

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('live', 'Live Performance'),
        ('weddings', 'Weddings'),
        ('corporate', 'Corporate Events'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='live')
    description = models.TextField(blank=True, help_text="Caption or description for this gallery item")
    image = models.ImageField(upload_to='portfolio_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    ROLE_CHOICES = [
        ('clarinet', 'Clarinet'),
        ('trumpet', 'Trumpet'),
        ('saxophone', 'Saxophone'),
        ('piano', 'Piano/Guitar'),
        ('bass', 'Bass Guitar'),
        ('drums', 'Drums'),
        ('vocals', 'Vocals'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True, help_text="Brief bio or description")
    image = models.ImageField(upload_to='team_images/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} - {self.role}"
