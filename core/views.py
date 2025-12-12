from django.shortcuts import render
from portfolio.models import Project

def index(request):
    projects = Project.objects.all()
    return render(request, 'core/index.html', {'projects': projects})

def service_details(request):
    return render(request, 'core/service_details.html')

def portfolio_details(request):
    return render(request, 'core/portfolio_details.html')
