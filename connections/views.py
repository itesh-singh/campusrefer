from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from accounts.models import User
from alumni.models import AlumniProfile
from core.models import Notification

from .forms import ConnectionRequestForm
from .models import ConnectionRequest


@login_required
def send_connection_request(request, alumni_id):
    if request.user.role != User.Roles.STUDENT:
        messages.error(request, "Only students can send connection requests.")
        return redirect("alumni:list")

    alumni_user = get_object_or_404(User, id=alumni_id, role=User.Roles.ALUMNI)
    get_object_or_404(AlumniProfile, user=alumni_user)

    existing_request = ConnectionRequest.objects.filter(
        student=request.user,
        alumni=alumni_user,
    ).first()

    if existing_request:
        messages.info(request, "You have already sent a request to this alumni.")
        return redirect("alumni:detail", pk=alumni_user.alumni_profile.pk)

    if request.method == "POST":
        form = ConnectionRequestForm(request.POST)
        if form.is_valid():
            connection_request = form.save(commit=False)
            connection_request.student = request.user
            connection_request.alumni = alumni_user
            connection_request.save()

            Notification.objects.create(
                user=alumni_user,
                message=f"{request.user.username} sent you a {connection_request.request_type} request.",
                link=reverse("connections:incoming_requests"),
            )

            messages.success(request, "Connection request sent successfully.")
            return redirect("alumni:detail", pk=alumni_user.alumni_profile.pk)
    else:
        form = ConnectionRequestForm()

    context = {
        "form": form,
        "alumni_user": alumni_user,
        "profile": alumni_user.alumni_profile,
    }
    return render(request, "connections/send_request.html", context)


@login_required
def incoming_requests_view(request):
    if request.user.role != User.Roles.ALUMNI:
        messages.error(request, "Only alumni can view incoming requests.")
        return redirect("core:home")

    requests = ConnectionRequest.objects.filter(alumni=request.user).select_related(
        "student",
        "student__student_profile",
    )
    return render(request, "connections/incoming_requests.html", {"requests": requests})


@login_required
def sent_requests_view(request):
    requests_qs = (
        ConnectionRequest.objects
        .filter(student=request.user)
        .select_related("alumni", "alumni__alumni_profile")
        .order_by("-created_at")
    )

    context = {
        "requests": requests_qs,
    }
    return render(request, "connections/sent_requests.html", context)


@login_required
def update_request_status(request, request_id, status):
    if request.user.role != User.Roles.ALUMNI:
        messages.error(request, "Only alumni can update request status.")
        return redirect("core:home")

    connection_request = get_object_or_404(
        ConnectionRequest,
        id=request_id,
        alumni=request.user,
    )

    if status not in [
        ConnectionRequest.Status.ACCEPTED,
        ConnectionRequest.Status.REJECTED,
    ]:
        messages.error(request, "Invalid request status.")
        return redirect("connections:incoming_requests")

    connection_request.status = status
    connection_request.save()

    Notification.objects.create(
        user=connection_request.student,
        message=f"Your {connection_request.request_type} request to {request.user.username} was {status}.",
        link=reverse("connections:sent_requests"),
    )

    messages.success(request, f"Request {status} successfully.")
    return redirect("connections:incoming_requests")