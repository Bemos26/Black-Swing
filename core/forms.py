from django import forms
from .models import ContactMessage, ServiceBooking

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Message'}),
        }

class ServiceBookingForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = ['client_name', 'email', 'phone', 'event_date', 'location', 'projected_cost', 'message']
        widgets = {
            'client_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Event Location'}),
            'projected_cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Estimated Budget (KES)'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Additional Details (Optional)'}),
        }
class ServiceBookingApprovalForm(forms.ModelForm):
    class Meta:
        model = ServiceBooking
        fields = ['projected_cost']
        widgets = {
            'projected_cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Confirmed Cost (KES)', 'required': 'required'}),
        }
