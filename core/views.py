from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Notification
from connections.models import ConnectionRequest
from jobs.models import JobPost
from alumni.models import AlumniProfile
from django.http import HttpResponse
from django.conf import settings
from .google_gmail_oauth import build_google_flow


def home_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect("adminpanel:dashboard")

    context = {}

    if request.user.is_authenticated:
        context["connection_requests_count"] = ConnectionRequest.objects.filter(
            student=request.user
        ).count()

        context["job_posts_count"] = JobPost.objects.count()
    
    context["featured_alumni"] = AlumniProfile.objects.select_related("user").all()[:2]
    return render(request, "core/home.html", context)


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


def google_gmail_connect_view(request):
    flow = build_google_flow()

    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    request.session["google_oauth_state"] = state
    request.session["google_oauth_code_verifier"] = flow.code_verifier

    return redirect(authorization_url)


def google_gmail_callback_view(request):
    state = request.session.get("google_oauth_state")
    code_verifier = request.session.get("google_oauth_code_verifier")

    if not state or not code_verifier:
        return HttpResponse("Missing OAuth session data. Start again from /google/email/connect/.", status=400)

    flow = build_google_flow()
    flow.redirect_uri = settings.GOOGLE_GMAIL_REDIRECT_URI
    flow.code_verifier = code_verifier

    flow.fetch_token(
        authorization_response=request.build_absolute_uri()
    )

    credentials = flow.credentials
    refresh_token = credentials.refresh_token

    request.session.pop("google_oauth_state", None)
    request.session.pop("google_oauth_code_verifier", None)

    if not refresh_token:
        return HttpResponse("No refresh token received. Remove app access and try again.", status=400)

    return HttpResponse(
        f"Refresh token copied below. Save it in .env as GOOGLE_GMAIL_REFRESH_TOKEN=<br><br><code>{refresh_token}</code>"
    )