import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'black_swing.settings')
django.setup()

from accounts.forms import TeacherRegistrationForm, StudentRegistrationForm

def check_form(FormClass, name):
    print(f"Checking {name}...")
    form = FormClass()
    for field in form:
        widget = field.field.widget
        print(f"Field: {field.name}, Widget: {type(widget).__name__}")
        try:
            print(f"  input_type: {widget.input_type}")
        except AttributeError:
            print(f"  NO input_type attribute!")

print("--- Starting Check ---")
try:
    check_form(TeacherRegistrationForm, "TeacherRegistrationForm")
    check_form(StudentRegistrationForm, "StudentRegistrationForm")
except Exception as e:
    print(f"Error: {e}")
