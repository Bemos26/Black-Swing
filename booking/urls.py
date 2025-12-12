from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_lesson, name='book_lesson'),
    path('update-status/<int:booking_id>/<str:status>/', views.update_booking_status, name='update_booking_status'),
]
