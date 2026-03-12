from django.conf import settings
from django.db import models


class ConnectionRequest(models.Model):
    class RequestType(models.TextChoices):
        MENTORSHIP = "mentorship", "Mentorship"
        REFERRAL = "referral", "Referral"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_connection_requests",
    )
    alumni = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_connection_requests",
    )
    request_type = models.CharField(
        max_length=20,
        choices=RequestType.choices,
    )
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("student", "alumni")

    def __str__(self):
        return f"{self.student.username} -> {self.alumni.username} ({self.request_type}, {self.status})"