from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Contact
from .utils import Mailer


@receiver(post_save, sender=Contact)
def send_email_alert_on_contact_save(sender, instance, created, **kwargs):
    if created:
        mailer = Mailer()
        mailer.contact_alert(instance)


