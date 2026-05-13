"""
Utility functions for the blood_request app.
"""
from .models import Notification
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random
import string
import datetime

def generate_unique_din():
    """Generates a unique Donor Identification Number (DIN)."""
    date_part = datetime.datetime.now().strftime('%Y%m%d')
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"DIN-{date_part}-{random_part}"

def send_din_email(recipient_email, din, record_type='donor'):
    """Sends the generated DIN to the user."""
    if not recipient_email:
        return

    subject = 'Your Udaan Society Identification Number (DIN)'
    
    if record_type == 'donor':
        message = f"Thank you for registering as a blood donor with Udaan Society.\n\nYour Request/Donor Identification Number (DIN) is: {din}\n\nPlease keep this number safe for future tracking.\n\nBest Regards,\nUdaan Society Team"
    else:
        message = f"Thank you for submitting a blood request to Udaan Society.\n\nYour Request Identification Number (DIN) is: {din}\n\nPlease keep this number safe to track your request.\n\nBest Regards,\nUdaan Society Team"

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email='mail@udaansociety.org',
            recipient_list=[recipient_email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send email: {e}")


def create_notification(user, message, link=None, actor=None):
    """
    Create a portal notification for a user.
    
    Args:
        user: The User receiving the notification
        message: Notification text
        link: Optional URL to navigate to when clicked
        actor: Optional User who triggered the notification
    """
    return Notification.objects.create(
        user=user,
        message=message,
        link=link or '',
        actor=actor,
    )
