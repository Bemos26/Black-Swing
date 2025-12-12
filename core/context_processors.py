from .models import ContactMessage, ServiceBooking

def unread_messages_count(request):
    if request.user.is_authenticated and request.user.is_superuser:
        messages_count = ContactMessage.objects.filter(is_read=False).count()
        bookings_count = ServiceBooking.objects.filter(is_read=False).count()
        return {'unread_messages_count': messages_count + bookings_count}
    return {}
