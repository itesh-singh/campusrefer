from functools import wraps
from django.core.paginator import Paginator

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import User
from django.db.models import Q
from alumni.models import AlumniProfile
from connections.models import ConnectionRequest
from jobs.models import JobPost
from students.models import StudentProfile

from django.utils import timezone
from datetime import timedelta
from django.db.models import Count


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

    today = timezone.now()
    last_7_days = today - timedelta(days=7)

    total_users = User.objects.count()
    total_students = User.objects.filter(role="student").count()
    total_alumni = User.objects.filter(role="alumni").count()

    verified_alumni = AlumniProfile.objects.filter(is_verified=True).count()
    verified_percent = 0
    if total_alumni:
        verified_percent = round((verified_alumni / total_alumni) * 100)

    total_jobs = JobPost.objects.count()
    active_jobs = JobPost.objects.filter(is_active=True).count()

    total_connections = ConnectionRequest.objects.count()
    accepted_connections = ConnectionRequest.objects.filter(status="accepted").count()

    success_rate = 0
    if total_connections:
        success_rate = round((accepted_connections / total_connections) * 100)

    new_users_7_days = User.objects.filter(date_joined__gte=last_7_days).count()

    top_companies = (
        JobPost.objects
        .values("company")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    context = {
        "total_users": total_users,
        "total_students": total_students,
        "total_alumni": total_alumni,
        "verified_percent": verified_percent,
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "total_connections": total_connections,
        "success_rate": success_rate,
        "new_users_7_days": new_users_7_days,
        "top_companies": top_companies,
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

    paginator = Paginator(users, 10)
    page_number = request.GET.get("page")
    users = paginator.get_page(page_number)

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

    paginator = Paginator(students, 10)
    page_number = request.GET.get("page")
    students = paginator.get_page(page_number)

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

    paginator = Paginator(alumni, 10)
    page_number = request.GET.get("page")
    alumni = paginator.get_page(page_number)

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

    jobs = JobPost.objects.select_related("alumni").annotate(
        applicants_count=Count("applications")
    ).order_by("-created_at")

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query) |
            Q(location__icontains=query) |
            Q(alumni__username__icontains=query)
        )

    paginator = Paginator(jobs, 10)
    page_number = request.GET.get("page")
    jobs = paginator.get_page(page_number)

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