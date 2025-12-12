from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

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
    return render(request, 'dashboard/admin_dashboard.html')

@login_required
def student_dashboard(request):
    if not request.user.is_student:
        return redirect('dashboard_redirect')
    return render(request, 'dashboard/student_dashboard.html')

@login_required
def teacher_dashboard(request):
    if not request.user.is_member:
        return redirect('dashboard_redirect')
    return render(request, 'dashboard/teacher_dashboard.html')
