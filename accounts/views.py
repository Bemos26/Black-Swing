from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import StudentRegistrationForm, UserLoginForm, TeacherRegistrationForm
from django.contrib import messages

def register_options(request):
    return render(request, 'accounts/register_options.html')

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Student registration successful.")
            return redirect('student_dashboard')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register_student.html', {'form': form})

def register_teacher(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Teacher registration successful! Please wait for approval.")
            return redirect('teacher_dashboard')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = TeacherRegistrationForm()
    return render(request, 'accounts/register_teacher.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Check if user is suspended
                if user.is_suspended:
                    messages.error(request, "Your account has been suspended. Please contact the administrator.")
                    return redirect('login')
                
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('dashboard_redirect')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('index')
