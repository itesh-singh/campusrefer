from django.urls import path
from . import views

app_name = "adminpanel"

urlpatterns = [
    path("", views.admin_dashboard, name="dashboard"),
    path("users/", views.admin_users, name="users"),
    path("students/", views.admin_students, name="students"),
    path("alumni/", views.admin_alumni, name="alumni"),
    path("alumni/<int:pk>/toggle-verify/", views.toggle_verify_alumni, name="toggle_verify_alumni"),
    path("jobs/", views.admin_jobs, name="jobs"),
    path("jobs/<int:pk>/toggle-active/", views.toggle_job_active, name="toggle_job_active"),
    path("users/<int:pk>/delete/", views.delete_user, name="delete_user"),
]