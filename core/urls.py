from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('service/<slug:slug>/', views.service_details, name='service_details'),
    path('portfolio-details/', views.portfolio_details, name='portfolio_details'),
    path('test-email/', views.test_email_view, name='test_email_view'),
]
