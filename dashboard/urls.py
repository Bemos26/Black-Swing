from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_redirect, name='dashboard_redirect'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/teachers/', views.manage_teachers, name='manage_teachers'),
    path('admin/teachers/delete/<int:profile_id>/', views.delete_teacher, name='delete_teacher'),
    path('admin/approve/<int:profile_id>/', views.approve_teacher, name='approve_teacher'),
    
    path('admin/projects/', views.manage_projects, name='manage_projects'),
    path('admin/projects/add/', views.add_project, name='add_project'),
    path('admin/projects/edit/<int:project_id>/', views.edit_project, name='edit_project'),
    path('admin/projects/delete/<int:project_id>/', views.delete_project, name='delete_project'),
    
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/apply/', views.apply_teacher, name='apply_teacher'),
    path('settings/', views.profile_settings, name='profile_settings'),
]
