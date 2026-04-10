from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import JobApplicationForm, JobPostForm
from .models import JobApplication, JobPost


@login_required
def job_list_view(request):

    query = request.GET.get("q", "").strip()
    company = request.GET.get("company", "").strip()
    location = request.GET.get("location", "").strip()
    job_type = request.GET.get("job_type", "").strip()

    jobs = JobPost.objects.filter(is_active=True).select_related("alumni").order_by("-created_at")

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query)
            | Q(company__icontains=query)
            | Q(location__icontains=query)
            | Q(description__icontains=query)
        )

    if company:
        jobs = jobs.filter(company__icontains=company)

    if location:
        jobs = jobs.filter(location__icontains=location)

    if job_type:
        jobs = jobs.filter(job_type__icontains=job_type)

    paginator = Paginator(jobs, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "jobs": page_obj,
        "page_obj": page_obj,
        "query": query,
        "company": company,
        "location": location,
        "job_type": job_type,
        "total_count": paginator.count,
    }
    return render(request, "jobs/job_list.html", context)


@login_required
def job_detail_view(request, pk):
    job = get_object_or_404(JobPost, pk=pk)

    already_applied = False
    if request.user.role == "student":
        already_applied = JobApplication.objects.filter(
            job=job,
            student=request.user,
        ).exists()

    return render(
        request,
        "jobs/job_detail.html",
        {
            "job": job,
            "already_applied": already_applied,
        },
    )


@login_required
def create_job_view(request):
    if request.user.role != "alumni":
        messages.error(request, "Only alumni can create job posts.")
        return redirect("jobs:list")

    if request.method == "POST":
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.alumni = request.user
            job.save()
            messages.success(request, "Job post created successfully.")
            return redirect("jobs:my_jobs")
    else:
        form = JobPostForm()

    return render(request, "jobs/create_job.html", {"form": form})


@login_required
def my_jobs_view(request):
    if request.user.role != "alumni":
        messages.error(request, "Only alumni can manage job posts.")
        return redirect("jobs:list")

    jobs = JobPost.objects.filter(alumni=request.user).annotate(
        applicants_count=Count("applications")
    )

    return render(request, "jobs/my_jobs.html", {"jobs": jobs})


@login_required
def edit_job_view(request, pk):
    if request.user.role != "alumni":
        messages.error(request, "Only alumni can edit job posts.")
        return redirect("jobs:list")

    job = get_object_or_404(JobPost, pk=pk, alumni=request.user)

    if request.method == "POST":
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job post updated successfully.")
            return redirect("jobs:my_jobs")
    else:
        form = JobPostForm(instance=job)

    return render(request, "jobs/edit_job.html", {"form": form, "job": job})


@login_required
def delete_job_view(request, pk):
    if request.user.role != "alumni":
        messages.error(request, "Only alumni can delete job posts.")
        return redirect("jobs:list")

    job = get_object_or_404(JobPost, pk=pk, alumni=request.user)

    if request.method == "POST":
        job.delete()
        messages.success(request, "Job post deleted successfully.")
        return redirect("jobs:my_jobs")

    return render(request, "jobs/delete_job.html", {"job": job})


@login_required
def apply_to_job_view(request, pk):
    job = get_object_or_404(JobPost, pk=pk, is_active=True)

    if request.user.role != "student":
        messages.error(request, "Only students can apply to jobs.")
        return redirect("jobs:detail", pk=job.pk)

    existing_application = JobApplication.objects.filter(
        job=job,
        student=request.user,
    ).first()

    if existing_application:
        messages.warning(request, "You have already applied to this job.")
        return redirect("jobs:detail", pk=job.pk)

    if request.method == "POST":
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.student = request.user
            application.save()

            from core.utils import create_notification
            create_notification(
                user=job.alumni,
                message=f"{request.user.username} applied for your job: {job.title} at {job.company}.",
                link=reverse("jobs:applicants", kwargs={"pk": job.pk}),
            )

            messages.success(request, "Application submitted successfully.")
            return redirect("jobs:my_applications")
    else:
        form = JobApplicationForm()

    return render(
        request,
        "jobs/apply.html",
        {
            "job": job,
            "form": form,
        },
    )


@login_required
def my_applications_view(request):
    if request.user.role != "student":
        messages.error(request, "Only students can view applications.")
        return redirect("core:home")

    applications = JobApplication.objects.select_related("job").filter(
        student=request.user
    )

    return render(
        request,
        "jobs/my_applications.html",
        {
            "applications": applications,
        },
    )


@login_required
def job_applicants_view(request, pk):
    if request.user.role != "alumni":
        messages.error(request, "Only alumni can view applicants.")
        return redirect("jobs:list")

    job = get_object_or_404(JobPost, pk=pk, alumni=request.user)

    applications = JobApplication.objects.select_related("student").filter(job=job)

    return render(
        request,
        "jobs/job_applicants.html",
        {
            "job": job,
            "applications": applications,
        },
    )


@login_required
def update_application_status_view(request, pk):
    if request.user.role != "alumni":
        messages.error(request, "Only alumni can update application status.")
        return redirect("jobs:list")

    application = get_object_or_404(
        JobApplication.objects.select_related("job"),
        pk=pk,
        job__alumni=request.user,
    )

    if request.method != "POST":
        messages.error(request, "Invalid request method.")
        return redirect("jobs:applicants", pk=application.job.pk)

    new_status = request.POST.get("status")

    valid_statuses = {"pending", "reviewed", "accepted", "rejected"}
    if new_status not in valid_statuses:
        messages.error(request, "Invalid status selected.")
        return redirect("jobs:applicants", pk=application.job.pk)

    application.status = new_status
    application.save()

    from core.utils import create_notification
    status_labels = {
        "reviewed": "has been reviewed",
        "accepted": "was accepted 🎉",
        "rejected": "was not selected",
        "pending": "is back to pending",
    }
    label = status_labels.get(new_status, f"was updated to {new_status}")
    create_notification(
        user=application.student,
        message=f"Your application for {application.job.title} at {application.job.company} {label}.",
        link=reverse("jobs:my_applications"),
    )

    messages.success(request, "Application status updated successfully.")
    return redirect("jobs:applicants", pk=application.job.pk)