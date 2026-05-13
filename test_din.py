import os
import django
import json
from django.test import RequestFactory
import sys

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from blood_request.views import register_donor, blood_request_create
from blood_request.models import BloodDonor, BloodRequest
from django.core import mail
from blood_request.utils import generate_unique_din, send_din_email

print("--- Testing Manual Utils ---")
din = generate_unique_din()
print(f"Generated DIN: {din}")
send_din_email('test@example.com', din, 'donor')
print(f"Email sent. Outbox length: {len(mail.outbox)}")
if len(mail.outbox) > 0:
    print(f"Email subject: {mail.outbox[0].subject}")
    print(f"Email body:\n{mail.outbox[0].body}")

mail.outbox = [] # reset

print("\n--- Testing API Views ---")
factory = RequestFactory()

# Test Donor Registration
donor_payload = {
    "name": "Test Donor",
    "blood_group": "A+",
    "phone": "9999999999",
    "email": "testdonor@example.com",
    "city": "Test City",
    "state": "Test State",
    "pin_code": "123456",
    "whatsapp_number": "9999999999",
    "email_notifications": True,
    "available_to_donate": True,
    "consent_given": True
}
request = factory.post('/api/register/', data=json.dumps(donor_payload), content_type='application/json')
response = register_donor(request)
print(f"Donor Registration Response: {response.content.decode()}")

donor = BloodDonor.objects.get(phone="9999999999")
print(f"Saved Donor DIN: {donor.din}")
print(f"Outbox length after donor: {len(mail.outbox)}")

# Test Blood Request
req_payload = {
    "city": "Request City",
    "pin_code": "654321",
    "blood_group": "O-",
    "units": "2",
    "address_line_2": "Test Address",
    "contact_person": "Jane Doe",
    "contact_phone": "8888888888",
    "contact_email": "testreq@example.com"
}
request = factory.post('/api/request/', data=json.dumps(req_payload), content_type='application/json')
response = blood_request_create(request)
print(f"Blood Request Response: {response.content.decode()}")

breq = BloodRequest.objects.get(contact_phone="8888888888")
print(f"Saved Request DIN: {breq.din}")
print(f"Outbox length after request: {len(mail.outbox)}")

# cleanup
donor.delete()
breq.delete()
