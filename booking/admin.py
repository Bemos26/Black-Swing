from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'lesson_type', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'lesson_type')
    search_fields = ('student__username', 'teacher__user__first_name')
