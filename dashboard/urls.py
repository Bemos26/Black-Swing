from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_redirect, name='dashboard_redirect'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/teachers/', views.manage_teachers, name='manage_teachers'),
    path('admin/teachers/delete/<int:profile_id>/', views.delete_teacher, name='delete_teacher'),
    path('admin/approve/<int:profile_id>/', views.approve_teacher, name='approve_teacher'),
    path('admin/booking/approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('admin/bookings/', views.manage_bookings, name='manage_bookings'),
    path('admin/booking/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('admin/message/<int:message_id>/', views.view_message, name='view_message'),
    
    path('admin/gallery/', views.manage_gallery, name='manage_gallery'),
    path('admin/gallery/add/', views.add_gallery_item, name='add_gallery_item'),
    path('admin/gallery/delete/<int:item_id>/', views.delete_gallery_item, name='delete_gallery_item'),
    
    path('admin/team/', views.manage_team, name='manage_team'),
    path('admin/team/add/', views.add_team_member, name='add_team_member'),
    path('admin/team/delete/<int:member_id>/', views.delete_team_member, name='delete_team_member'),
    
    path('admin/users/', views.manage_users, name='manage_users'),
    path('admin/users/suspend/<int:user_id>/', views.suspend_user, name='suspend_user'),
    path('admin/users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/apply/', views.apply_teacher, name='apply_teacher'),
    path('settings/', views.profile_settings, name='profile_settings'),
]
