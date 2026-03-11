from django.conf import settings
from django.db import models


class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    full_name = models.CharField(max_length=150)
    year = models.PositiveIntegerField()
    branch = models.CharField(max_length=100)
    skills = models.TextField(blank=True)
    target_role = models.CharField(max_length=100, blank=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.full_name