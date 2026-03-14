from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.models import User
from connections.models import ConnectionRequest
from jobs.models import JobPost


@login_required
def dashboard_redirect_view(request):
    if request.user.is_superuser:
        return redirect("adminpanel:dashboard")
    if request.user.role == User.Roles.STUDENT:
        return redirect("dashboards:student_dashboard")
    if request.user.role == User.Roles.ALUMNI:
        return redirect("dashboards:alumni_dashboard")
    return redirect("core:home")


@login_required
def student_dashboard_view(request):
    if request.user.role != User.Roles.STUDENT:
        return redirect("core:home")

    sent_requests = ConnectionRequest.objects.filter(student=request.user)
    recent_jobs = JobPost.objects.all()[:5]

    context = {
        "total_sent_requests": sent_requests.count(),
        "accepted_requests": sent_requests.filter(status=ConnectionRequest.Status.ACCEPTED).count(),
        "pending_requests": sent_requests.filter(status=ConnectionRequest.Status.PENDING).count(),
        "rejected_requests": sent_requests.filter(status=ConnectionRequest.Status.REJECTED).count(),
        "recent_jobs": recent_jobs,
    }
    return render(request, "dashboards/student_dashboard.html", context)


@login_required
def alumni_dashboard_view(request):
    if request.user.role != User.Roles.ALUMNI:
        return redirect("core:home")

    incoming_requests = ConnectionRequest.objects.filter(alumni=request.user)
    my_jobs = JobPost.objects.filter(alumni=request.user)

    context = {
        "total_incoming_requests": incoming_requests.count(),
        "pending_requests": incoming_requests.filter(status=ConnectionRequest.Status.PENDING).count(),
        "accepted_requests": incoming_requests.filter(status=ConnectionRequest.Status.ACCEPTED).count(),
        "rejected_requests": incoming_requests.filter(status=ConnectionRequest.Status.REJECTED).count(),
        "total_job_posts": my_jobs.count(),
        "recent_incoming_requests": incoming_requests[:5],
        "profile_views": request.user.alumni_profile.profile_views,
    }
    return render(request, "dashboards/alumni_dashboard.html", context)