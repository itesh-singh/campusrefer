from django.urls import path

from .views import (
    alumni_dashboard_view,
    dashboard_redirect_view,
    student_dashboard_view,
)

app_name = "dashboards"

urlpatterns = [
    path("", dashboard_redirect_view, name="dashboard_redirect"),
    path("student/", student_dashboard_view, name="student_dashboard"),
    path("alumni/", alumni_dashboard_view, name="alumni_dashboard"),
]