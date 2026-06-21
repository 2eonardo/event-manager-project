from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('attendee', 'Attendee'),
        ('organizer', 'Organizer'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, blank=False)
    bio = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"