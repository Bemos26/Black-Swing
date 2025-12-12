from django.db import models
from django.conf import settings
from accounts.models import MemberProfile

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    LESSON_TYPES = [
        ('guitar', 'Guitar'),
        ('piano', 'Piano'),
        ('drums', 'Drums'),
        ('vocals', 'Vocals'),
        ('production', 'Music Production'),
    ]

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    teacher = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='teacher_bookings')
    lesson_type = models.CharField(max_length=50, choices=LESSON_TYPES)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.lesson_type} - {self.student.username} with {self.teacher.user.first_name} on {self.date}"
