from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Notification


def home_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("adminpanel:dashboard")
    return render(request, "core/home.html")


@login_required
def profile_redirect_view(request):
    if request.user.is_superuser:
        return redirect("adminpanel:dashboard")
    if request.user.role == "student":
        return redirect("students:edit_profile")
    if request.user.role == "alumni":
        return redirect("alumni:edit_profile")
    return redirect("core:home")


@login_required
def notifications_view(request):
    notifications = request.user.notifications.all()
    unread_notifications = notifications.filter(is_read=False)
    unread_notifications.update(is_read=True)

    return render(
        request,
        "core/notifications.html",
        {"notifications": notifications},
    )