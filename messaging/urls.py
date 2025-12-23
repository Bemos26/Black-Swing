from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.teacher_chat_view, name='teacher_chat'),
    path('inbox/', views.admin_inbox_view, name='admin_inbox'),
    path('inbox/<int:user_id>/', views.admin_chat_detail_view, name='admin_chat_detail'),
]
