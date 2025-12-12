from django.db import models

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('app', 'App'),
        ('product', 'Product'),
        ('branding', 'Branding'),
        ('books', 'Books'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='app')
    client = models.CharField(max_length=200, blank=True)
    project_date = models.DateField(auto_now_add=True)
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='portfolio_images/')

    def __str__(self):
        return self.title
