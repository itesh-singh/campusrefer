from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import JobApplicationForm, JobPostForm
from .models import JobApplication, JobPost


@login_required
def job_list_view(request):
    jobs = JobPost.objects.filter(is_active=True).select_related("alumni")
    return render(request, "jobs/job_list.html", {"jobs": jobs})


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

    jobs = JobPost.objects.filter(alumni=request.user)
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