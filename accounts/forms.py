from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser, MemberProfile

class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    pass

class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['role', 'bio', 'image', 'twitter_link', 'facebook_link', 'instagram_link', 'linkedin_link']
        widgets = {
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Piano Teacher'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'twitter_link': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook_link': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram_link': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin_link': forms.URLInput(attrs={'class': 'form-control'}),
        }
