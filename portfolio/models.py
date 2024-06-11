import uuid

from django.db import models


class Site(models.Model):
    client_id = models.UUIDField(primary_key=True, auto_created=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    url = models.URLField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    contact_receiver_email = models.EmailField(null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    site = models.ForeignKey('Site', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.site.name} - {self.created_at}"


class Resume(models.Model):
    key = models.UUIDField(unique=True, auto_created=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    site = models.ForeignKey('Site', on_delete=models.CASCADE)
    url = models.URLField(blank=False, null=False)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
