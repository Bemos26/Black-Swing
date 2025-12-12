from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_redirect, name='dashboard_redirect'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/approve/<int:profile_id>/', views.approve_teacher, name='approve_teacher'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/apply/', views.apply_teacher, name='apply_teacher'),
]
