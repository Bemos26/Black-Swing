from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'project_date')
    list_filter = ('category', 'project_date')
    search_fields = ('title', 'description', 'client')
