from django.shortcuts import render

def index(request):
    return render(request, 'core/index.html')

def service_details(request):
    return render(request, 'core/service_details.html')

def portfolio_details(request):
    return render(request, 'core/portfolio_details.html')
