from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    AlumniDetailView,
    AlumniListView,
    ConnectionListView,
    JobDetailView,
    JobListView,
    MyProfileView,
    NotificationListView,
    RegisterView,
    SendConnectionRequestView,
)

app_name = "api"

urlpatterns = [
    # Auth
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Profile
    path("profile/", MyProfileView.as_view(), name="my_profile"),

    # Alumni
    path("alumni/", AlumniListView.as_view(), name="alumni_list"),
    path("alumni/<int:pk>/", AlumniDetailView.as_view(), name="alumni_detail"),

    # Jobs
    path("jobs/", JobListView.as_view(), name="job_list"),
    path("jobs/<int:pk>/", JobDetailView.as_view(), name="job_detail"),

    # Connections
    path("connections/", ConnectionListView.as_view(), name="connection_list"),
    path("connections/send/<int:alumni_id>/", SendConnectionRequestView.as_view(), name="send_connection"),

    # Notifications
    path("notifications/", NotificationListView.as_view(), name="notifications"),
]