from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("profile/", views.profile_redirect_view, name="profile_redirect"),
    path("notifications/", views.notifications_view, name="notifications"),
    path("google/email/connect/", views.google_gmail_connect_view, name="google_gmail_connect"),
    path("accounts/google/login/callback/", views.google_gmail_callback_view, name="google_gmail_callback"),
]