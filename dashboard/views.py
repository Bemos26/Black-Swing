from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import MemberProfile, CustomUser
from accounts.forms import MemberProfileForm, UserUpdateForm
from booking.models import Booking
from core.models import ServiceBooking, ContactMessage
from django.core.mail import send_mail
from django.conf import settings
from portfolio.models import Project
from portfolio.forms import ProjectForm

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
    
    # Get pending service bookings
    pending_service_bookings = ServiceBooking.objects.filter(status='Pending')
    
    # Get unread contact messages
    unread_messages = ContactMessage.objects.filter(is_read=False)
    
    # Statistics
    total_users = CustomUser.objects.count()
    total_teachers = MemberProfile.objects.filter(is_approved=True).count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    
    context = {
        'pending_teachers': pending_teachers,
        'pending_service_bookings': pending_service_bookings,
        'unread_messages': unread_messages,
        'total_users': total_users,
        'total_teachers': total_teachers,
        'pending_bookings': pending_bookings,
    }
    
    
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def manage_teachers(request):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
    
    teachers = MemberProfile.objects.all().order_by('is_approved', 'user__first_name')
    return render(request, 'dashboard/manage_teachers.html', {'teachers': teachers})

@login_required
def delete_teacher(request, profile_id):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
    
    profile = get_object_or_404(MemberProfile, id=profile_id)
    user = profile.user
    
    # Delete profile and user
    user.delete()
    
    messages.success(request, "Teacher account deleted successfully.")
    return redirect('manage_teachers')

@login_required
def approve_teacher(request, profile_id):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
    
    profile = get_object_or_404(MemberProfile, id=profile_id)
    profile.is_approved = True
    profile.save()
    
    # Send Approval Email
    subject = 'Welcome to the Team! - Black Swing'
    message = f"""
    Dear {profile.user.first_name},

    Congratulations! Your application to join Black Swing as a {profile.role} has been approved.
    
    You can now log in to your dashboard to manage your schedule and profile.

    Best regards,
    Black Swing Team
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'info@blackswing.com',
        [profile.user.email],
        fail_silently=False,
    )
    
    messages.success(request, f"{profile.user.first_name}'s profile approved and email sent.")
    return redirect('manage_teachers') # Redirect to list instead of dash

@login_required
def manage_projects(request):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
    projects = Project.objects.all().order_by('-project_date')
    return render(request, 'dashboard/manage_projects.html', {'projects': projects})

@login_required
def add_project(request):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Project added successfully.")
            return redirect('manage_projects')
    else:
        form = ProjectForm()
    return render(request, 'dashboard/project_form.html', {'form': form, 'title': 'Add Project'})

@login_required
def edit_project(request, project_id):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
    
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully.")
            return redirect('manage_projects')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'dashboard/project_form.html', {'form': form, 'title': 'Edit Project'})

@login_required
def delete_project(request, project_id):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
    
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    messages.success(request, "Project deleted successfully.")
    return redirect('manage_projects')

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
        # Redirect to application page if no profile (for existing users who want to upgrade)
        return redirect('apply_teacher')

    if not request.user.is_member:
        return redirect('dashboard_redirect')
    
    # Pass profile to template to check is_approved
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

@login_required
def profile_settings(request):
    user = request.user
    
    # Init forms
    user_form = UserUpdateForm(instance=user)
    profile_form = None
    
    if user.is_member and hasattr(user, 'member_profile'):
        profile_form = MemberProfileForm(instance=user.member_profile)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        valid = user_form.is_valid()
        
        if profile_form:
            profile_form = MemberProfileForm(request.POST, request.FILES, instance=user.member_profile)
            valid = valid and profile_form.is_valid()
        
        if valid:
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile_settings')
            
    return render(request, 'dashboard/settings.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
