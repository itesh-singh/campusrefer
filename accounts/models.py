from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        STUDENT = "student", "Student"
        ALUMNI = "alumni", "Alumni"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Roles.choices)

    def __str__(self):
        return f"{self.username} ({self.role})"