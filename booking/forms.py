from django import forms
from .models import Booking
from accounts.models import MemberProfile

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['teacher', 'lesson_type', 'date', 'time', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'lesson_type': forms.Select(attrs={'class': 'form-control'}),
            'teacher': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter teachers roughly by role if needed, or just show all MemberProfiles
        self.fields['teacher'].queryset = MemberProfile.objects.filter(is_approved=True)
        self.fields['teacher'].label_from_instance = lambda obj: f"{obj.user.first_name} {obj.user.last_name} ({obj.role})"
