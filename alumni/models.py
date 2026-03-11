from django.conf import settings
from django.db import models


class AlumniProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="alumni_profile",
    )
    full_name = models.CharField(max_length=150)
    batch_year = models.PositiveIntegerField()
    branch = models.CharField(max_length=100)
    current_company = models.CharField(max_length=150, blank=True)
    current_role = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True)
    open_to_mentorship = models.BooleanField(default=False)
    open_to_referrals = models.BooleanField(default=False)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.full_name