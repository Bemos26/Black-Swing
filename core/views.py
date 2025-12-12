from django.shortcuts import render, get_object_or_404, redirect
from portfolio.models import Project, TeamMember
from .models import Service, ServiceBooking
from .forms import ContactForm, ServiceBookingForm
from django.contrib import messages

def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent. Thank you!')
            return redirect('index')
    else:
        form = ContactForm()

    projects = Project.objects.all().order_by('-created_at')
    team_members = TeamMember.objects.filter(is_active=True).order_by('order', 'name')
    services = Service.objects.all()
    # Fallback if no services exist yet (for initial load safety)
    if not services:
        services = [] 
        
    return render(request, 'core/index.html', {
        'projects': projects, 
        'team_members': team_members,
        'form': form,
        'services': services
    })

def service_details(request, slug):
    service = get_object_or_404(Service, slug=slug)
    
    if request.method == 'POST':
        form = ServiceBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.service = service
            booking.save()
            messages.success(request, f'Booking request for {service.title} sent successfully! We will contact you soon.')
            return redirect('service_details', slug=slug)
    else:
        form = ServiceBookingForm()

    return render(request, 'core/service_details.html', {
        'service': service,
        'form': form
    })

def portfolio_details(request):
    return render(request, 'core/portfolio_details.html')
