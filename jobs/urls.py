from django.urls import path

from .views import (
    apply_to_job_view,
    create_job_view,
    delete_job_view,
    edit_job_view,
    job_applicants_view,
    job_detail_view,
    job_list_view,
    my_applications_view,
    my_jobs_view,
    update_application_status_view,
)

app_name = "jobs"

urlpatterns = [
    path("", job_list_view, name="list"),
    path("create/", create_job_view, name="create"),
    path("my-jobs/", my_jobs_view, name="my_jobs"),
    path("my-applications/", my_applications_view, name="my_applications"),
    path("applications/<int:pk>/status/", update_application_status_view, name="update_application_status"),
    path("<int:pk>/", job_detail_view, name="detail"),
    path("<int:pk>/apply/", apply_to_job_view, name="apply"),
    path("<int:pk>/applicants/", job_applicants_view, name="applicants"),
    path("<int:pk>/edit/", edit_job_view, name="edit"),
    path("<int:pk>/delete/", delete_job_view, name="delete"),
]