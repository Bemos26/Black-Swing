from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .forms import BookingForm

@login_required
def book_lesson(request):
    if not request.user.is_student:
        messages.warning(request, "Only students can book lessons.")
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.student = request.user
            booking.save()
            messages.success(request, "Booking request sent successfully!")
            return redirect('student_dashboard')
    else:
        form = BookingForm()
    
    return render(request, 'booking/book_lesson.html', {'form': form})

@login_required
def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Security check: Ensure the user is the teacher for this booking
    if not hasattr(request.user, 'member_profile') or booking.teacher != request.user.member_profile:
        messages.error(request, "You are not authorized to manage this booking.")
        return redirect('dashboard_redirect')
    
    if status in ['confirmed', 'cancelled', 'completed']:
        booking.status = status
        booking.save()
        messages.success(request, f"Booking {status}.")
    
    return redirect('teacher_dashboard')
