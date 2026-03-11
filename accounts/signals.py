from django.db.models.signals import post_save
from django.dispatch import receiver

from alumni.models import AlumniProfile
from students.models import StudentProfile

from .models import User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.role == User.Roles.STUDENT:
        StudentProfile.objects.create(
            user=instance,
            full_name=instance.username,
            year=1,
            branch="",
        )
    elif instance.role == User.Roles.ALUMNI:
        AlumniProfile.objects.create(
            user=instance,
            full_name=instance.username,
            batch_year=2020,
            branch="",
        )