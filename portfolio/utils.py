import smtplib

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import Contact


class Mailer:
    def __init__(self):
        self.sender = settings.EMAIL_SENDER

    def send_email(self, subject, message, recipient_list, template=None):
        try:
            send_mail(
                subject,
                message,
                self.sender,
                recipient_list,
                html_message=template,
                fail_silently=False,
            )
        except smtplib.SMTPException as e:

            return False  # mail not sent

    def contact_alert(self, contact: Contact):
        subject = f'New Contact Alert - {contact.site.name}'
        message = f'New Contact from {contact.name}'
        recipient_list = [contact.site.contact_receiver_email] if contact.site.contact_receiver_email else [
            contact.site.user.email]
        template = render_to_string('emails/contact.html', {'contact': contact})
        self.send_email(subject, message, recipient_list, template)
        return True  # mail sent successfully
