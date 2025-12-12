from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_redirect, name='dashboard_redirect'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
]
