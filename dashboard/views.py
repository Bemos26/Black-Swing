from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import MemberProfile
from accounts.forms import MemberProfileForm

@login_required
def dashboard_redirect(request):
    user = request.user
    if user.is_superuser:
        return redirect('admin_dashboard')
    elif user.is_member:
        return redirect('teacher_dashboard')
    elif user.is_student:
        return redirect('student_dashboard')
    else:
        # Fallback
        return redirect('index')

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
    
    # Get pending teachers
    pending_teachers = MemberProfile.objects.filter(is_approved=False)
    
    return render(request, 'dashboard/admin_dashboard.html', {'pending_teachers': pending_teachers})

@login_required
def approve_teacher(request, profile_id):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
    
    profile = get_object_or_404(MemberProfile, id=profile_id)
    profile.is_approved = True
    profile.save()
    
    messages.success(request, f"{profile.user.first_name}'s profile approved.")
    return redirect('admin_dashboard')

@login_required
def student_dashboard(request):
    if not request.user.is_student:
        return redirect('dashboard_redirect')
    bookings = request.user.bookings.all().order_by('-date')
    return render(request, 'dashboard/student_dashboard.html', {'bookings': bookings})

@login_required
def teacher_dashboard(request):
    # Check if user has a profile
    try:
        profile = request.user.member_profile
    except MemberProfile.DoesNotExist:
        # Redirect to application page if no profile
        return redirect('apply_teacher')

    if not request.user.is_member:
        # If they aren't marked as member yet (shouldn't happen if profile exists, but safety check)
        return redirect('dashboard_redirect')
    
    bookings = profile.teacher_bookings.all().order_by('-date')
    return render(request, 'dashboard/teacher_dashboard.html', {'bookings': bookings, 'profile': profile})

@login_required
def apply_teacher(request):
    if request.method == 'POST':
        form = MemberProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            
            # Update user status
            request.user.is_member = True
            request.user.save()
            
            messages.success(request, "Application submitted! Please wait for admin approval.")
            return redirect('teacher_dashboard')
    else:
        form = MemberProfileForm()
    
    return render(request, 'dashboard/apply_teacher.html', {'form': form})
