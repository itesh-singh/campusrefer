from functools import wraps

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from django.db.models import Q
from alumni.models import AlumniProfile
from connections.models import ConnectionRequest
from jobs.models import JobPost
from students.models import StudentProfile


def superuser_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, "Access denied.")
            return redirect("core:home")
        return view_func(request, *args, **kwargs)
    return wrapper


@superuser_required
def admin_dashboard(request):
    context = {
        "total_users": User.objects.count(),
        "total_students": User.objects.filter(role="student").count(),
        "total_alumni": User.objects.filter(role="alumni").count(),
        "total_jobs": JobPost.objects.count(),
        "active_jobs": JobPost.objects.filter(is_active=True).count(),
        "total_connections": ConnectionRequest.objects.count(),
        "pending_connections": ConnectionRequest.objects.filter(status="pending").count(),
        "accepted_connections": ConnectionRequest.objects.filter(status="accepted").count(),
        "recent_users": User.objects.order_by("-date_joined")[:10],
        "recent_jobs": JobPost.objects.order_by("-created_at")[:5],
        "recent_connections": ConnectionRequest.objects.order_by("-created_at")[:5],
    }
    return render(request, "adminpanel/dashboard.html", context)


@superuser_required
def admin_users(request):
    query = request.GET.get("q", "").strip()

    users = User.objects.order_by("-date_joined")

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(role__icontains=query)
        )

    return render(
        request,
        "adminpanel/users.html",
        {
            "users": users,
            "query": query,
        },
    )


@superuser_required
def admin_students(request):
    query = request.GET.get("q", "").strip()

    students = StudentProfile.objects.select_related("user").order_by("full_name")

    if query:
        students = students.filter(
            Q(full_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query) |
            Q(branch__icontains=query) |
            Q(target_role__icontains=query) |
            Q(skills__icontains=query)
        )

    return render(
        request,
        "adminpanel/students.html",
        {
            "students": students,
            "query": query,
        },
    )


@superuser_required
def admin_alumni(request):
    query = request.GET.get("q", "").strip()

    alumni = AlumniProfile.objects.select_related("user").order_by("full_name")

    if query:
        alumni = alumni.filter(
            Q(full_name__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query) |
            Q(current_company__icontains=query) |
            Q(current_role__icontains=query) |
            Q(city__icontains=query)
        )

    return render(
        request,
        "adminpanel/alumni.html",
        {
            "alumni": alumni,
            "query": query,
        },
    )


@superuser_required
def toggle_verify_alumni(request, pk):
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("adminpanel:alumni")

    profile = get_object_or_404(AlumniProfile, pk=pk)
    profile.is_verified = not profile.is_verified
    profile.save()

    messages.success(
        request,
        f"{profile.full_name} {'verified' if profile.is_verified else 'unverified'} successfully."
    )
    return redirect("adminpanel:alumni")


@superuser_required
def admin_jobs(request):
    query = request.GET.get("q", "").strip()

    jobs = JobPost.objects.select_related("alumni").order_by("-created_at")

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query) |
            Q(location__icontains=query) |
            Q(alumni__username__icontains=query)
        )

    return render(
        request,
        "adminpanel/jobs.html",
        {
            "jobs": jobs,
            "query": query,
        },
    )


@superuser_required
def toggle_job_active(request, pk):
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("adminpanel:jobs")

    job = get_object_or_404(JobPost, pk=pk)
    job.is_active = not job.is_active
    job.save()

    messages.success(
        request,
        f"Job {'activated' if job.is_active else 'deactivated'} successfully."
    )
    return redirect("adminpanel:jobs")


@superuser_required
def delete_user(request, pk):
    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("adminpanel:users")

    user = get_object_or_404(User, pk=pk)

    if user.is_superuser:
        messages.error(request, "Cannot delete superuser.")
        return redirect("adminpanel:users")

    user.delete()
    messages.success(request, "User deleted successfully.")
    return redirect("adminpanel:users")