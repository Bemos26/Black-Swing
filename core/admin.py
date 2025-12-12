from django.contrib import admin
from .models import ContactMessage, Service, ServiceBooking

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

from django.contrib import admin
from .models import ContactMessage, Service, ServiceBooking
from django.core.mail import send_mail
from django.conf import settings

@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ('service', 'client_name', 'event_date', 'status', 'projected_cost', 'created_at')
    list_filter = ('status', 'event_date', 'service')
    search_fields = ('client_name', 'email', 'location')
    readonly_fields = ('created_at',)
    
    actions = ['mark_as_read']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected bookings as read"

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = ServiceBooking.objects.get(pk=obj.pk)
            if old_obj.status != 'Approved' and obj.status == 'Approved':
                # Status changed to Approved, send email
                subject = f'Booking Confirmed: {obj.service.title}'
                message = f"""
                Dear {obj.client_name},

                We are pleased to confirm your booking for {obj.service.title}.

                Details:
                Date: {obj.event_date}
                Location: {obj.location}
                Confirmed Cost: KES {obj.projected_cost}

                Thank you for choosing Black Swing!

                Best regards,
                Black Swing Team
                """
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'info@blackswing.com',
                    [obj.email],
                    fail_silently=False,
                )
        super().save_model(request, obj, form, change)
