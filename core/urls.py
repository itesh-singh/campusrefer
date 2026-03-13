from django.urls import path

from .views import home_view, notifications_view, profile_redirect_view

app_name = "core"

urlpatterns = [
    path("", home_view, name="home"),
    path("profile/", profile_redirect_view, name="profile_redirect"),
    path("notifications/", notifications_view, name="notifications"),
]