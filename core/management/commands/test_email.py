from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings
import smtplib

class Command(BaseCommand):
    help = 'Tests email sending configuration'

    def add_arguments(self, parser):
        parser.add_argument('recipient', type=str, help='Email address to send test email to')

    def handle(self, *args, **kwargs):
        recipient = kwargs['recipient']
        self.stdout.write(f"Attempting to send email to {recipient}...")
        self.stdout.write(f"Using HOST: {settings.EMAIL_HOST}")
        self.stdout.write(f"Using PORT: {settings.EMAIL_PORT}")
        self.stdout.write(f"Using USER: {settings.EMAIL_HOST_USER}")
        # Don't print the password!

        try:
            send_mail(
                'Test Email from Black Swing',
                'This is a test email to verify correct SMTP configuration.',
                settings.DEFAULT_FROM_EMAIL,
                [recipient],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully sent email to {recipient}'))
        except smtplib.SMTPAuthenticationError:
            self.stdout.write(self.style.ERROR('SMTP Authentication Error: Check your EMAIL_HOST_USER and EMAIL_HOST_PASSWORD.'))
            self.stdout.write(self.style.ERROR('NOTE: If using Gmail, ensure you are using an App Password, not your login password.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send email: {str(e)}'))
