from django.urls import path

from .views import CustomLoginView, LogoutView, forgot_password_view, register_view, reset_password_view, verify_email_view

app_name = "accounts"

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("verify-email/<uidb64>/<token>/", verify_email_view, name="verify_email"),
    path("forgot-password/", forgot_password_view, name="forgot_password"),
    path("reset-password/<uidb64>/<token>/",reset_password_view,name="reset_password",),
]