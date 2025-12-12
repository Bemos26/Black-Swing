from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import MemberProfile, CustomUser
from accounts.forms import MemberProfileForm, UserUpdateForm
from booking.models import Booking
from core.models import ServiceBooking, ContactMessage
from core.forms import ServiceBookingApprovalForm
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from portfolio.models import Project, TeamMember
from portfolio.forms import ProjectForm, TeamMemberForm
import threading

class EmailThread(threading.Thread):
    def __init__(self, subject, html_content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(
            self.subject, 
            self.html_content, 
            settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'info@blackswing.com', 
            self.recipient_list
        )
        msg.content_subtype = "html" # Main content is now text/html
        try:
            msg.send()
        except Exception as e:
            # In a real app, log this error
            print(f"Error sending email: {e}")

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
    
    # Get pending teachers - OPTIMIZED: select_related('user')
    pending_teachers = MemberProfile.objects.filter(is_approved=False).select_related('user')[:10]
    
    # Get pending service bookings - OPTIMIZED: select_related('service')
    # Get pending service bookings - OPTIMIZED: select_related('service')
    # We pass the queryset directly to avoid instantiating forms for every item in the loop.
    # The form field rendering will be handled manually in the template.
    pending_service_bookings = ServiceBooking.objects.filter(status='Pending').select_related('service')[:10]
    
    # Get unread contact messages
    unread_messages = ContactMessage.objects.filter(is_read=False)

    # RECENT ACTIVITY (Approvals)
    # Bookings: Approved, newest updated (approved) first
    recent_approved_bookings = ServiceBooking.objects.filter(status='Approved').select_related('service').order_by('-updated_at')[:5]
    # Teachers: Approved, newest joined first
    recent_approved_teachers = MemberProfile.objects.filter(is_approved=True).select_related('user').order_by('-user__date_joined')[:5]
    
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
        'recent_approved_bookings': recent_approved_bookings,
        'recent_approved_teachers': recent_approved_teachers,
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
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Teacher account deleted successfully.'})
        
    return redirect('manage_teachers')

@login_required
def approve_booking(request, booking_id):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
        
    booking = get_object_or_404(ServiceBooking, id=booking_id)
    
    if request.method == 'POST':
        form = ServiceBookingApprovalForm(request.POST, instance=booking)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.status = 'Approved'
            booking.is_read = True  # Mark as read
            booking.save()
            
            # Send Approval Email (Async)
            subject = f'Booking Confirmed: {booking.service.title}'
            message = f"""
            Dear {booking.client_name},<br><br>

            We are pleased to confirm your booking for <strong>{booking.service.title}</strong>.<br><br>

            <strong>Details:</strong><br>
            Date: {booking.event_date}<br>
            Location: {booking.location}<br>
            Confirmed Cost: KES {booking.projected_cost}<br><br>

            Thank you for choosing Black Swing!<br><br>

            Best regards,<br>
            Black Swing Team
            """
            # Note: The original message was plain text, but EmailThread assumes HTML or we can just send as plain if we adjust the class.
            # Let's keep it simple and use EmailThread which I defined to handle sending.
            # Since I defined EmailThread to use EmailMessage, let's treat the message as the body.
            # I'll update the body to slightly better HTML formatting for valid email.
            
            EmailThread(subject, message, [booking.email]).start()
            
            messages.success(request, f"Booking for {booking.client_name} approved and email sent.")
        else:
            messages.error(request, "Error approving booking. Please check details.")
            
    return redirect('admin_dashboard')

@login_required
def delete_booking(request, booking_id):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
    
    booking = get_object_or_404(ServiceBooking, id=booking_id)
    booking.delete()
    messages.success(request, "Booking deleted successfully.")
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Booking deleted successfully.'})
        
    # Redirect back to where they came from if possible, or dashboard
    return redirect('admin_dashboard')

@login_required
def approve_teacher(request, profile_id):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
    
    profile = get_object_or_404(MemberProfile, id=profile_id)
    profile.is_approved = True
    profile.save()
    
    # Send Approval Email (Async)
    subject = 'Welcome to the Team! - Black Swing'
    message = f"""
    Dear {profile.user.first_name},<br><br>

    Congratulations! Your application to join Black Swing as a <strong>{profile.role}</strong> has been approved.<br><br>
    
    You can now log in to your dashboard to manage your schedule and profile.<br><br>

    Best regards,<br>
    Black Swing Team
    """
    EmailThread(subject, message, [profile.user.email]).start()
    
    messages.success(request, f"{profile.user.first_name}'s profile approved and email sent.")
    return redirect('manage_teachers')

@login_required
def manage_bookings(request):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
        
    # Fetch all bookings, ordered by newest first
    bookings = ServiceBooking.objects.all().order_by('-created_at')
    
    return render(request, 'dashboard/manage_bookings.html', {'bookings': bookings})

@login_required
def view_message(request, message_id):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
        
    message = get_object_or_404(ContactMessage, id=message_id)
    
    # Mark as read
    if not message.is_read:
        message.is_read = True
        message.save()
        
    # For now, we can redirect back to dashboard or render a detail view.
    # Since the user just wanted to view it and clear notification, let's show a simple detail page or redirect.
    # To keep it simple and effective, let's redirect to a message detail modal or page. 
    # But wait, the user said "view them". Let's assume they might want to read a long message.
    # I'll create a simple message detail template or reuse dashboard with a modal? 
    # Actually, a separate simple page is cleaner for "viewing".
    return render(request, 'dashboard/message_detail.html', {'message': message}) # Redirect to list instead of dash

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

@login_required
def manage_gallery(request):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
    items = Project.objects.all().order_by('-created_at')
    return render(request, 'dashboard/manage_gallery.html', {'items': items})

@login_required
def add_gallery_item(request):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Gallery item added successfully.")
            return redirect('manage_gallery')
    else:
        form = ProjectForm()
    
    return render(request, 'dashboard/add_gallery_item.html', {'form': form})

@login_required
def delete_gallery_item(request, item_id):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
        
    item = get_object_or_404(Project, id=item_id)
    item.delete()
    messages.success(request, "Gallery item deleted successfully.")
    return redirect('manage_gallery')

@login_required
def manage_team(request):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
    members = TeamMember.objects.all().order_by('order', 'name')
    return render(request, 'dashboard/manage_team.html', {'members': members})

@login_required
def add_team_member(request):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
    
    if request.method == 'POST':
        form = TeamMemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Team member added successfully.")
            return redirect('manage_team')
    else:
        form = TeamMemberForm()
    
    return render(request, 'dashboard/add_team_member.html', {'form': form})

@login_required
def delete_team_member(request, member_id):
    if not request.user.is_superuser:
        return redirect('dashboard_redirect')
        
    member = get_object_or_404(TeamMember, id=member_id)
    member.delete()
    messages.success(request, "Team member deleted successfully.")
    return redirect('manage_team')
