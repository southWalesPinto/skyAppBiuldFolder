from django.contrib import admin
from django.contrib.auth.views import (
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import include, path, reverse_lazy

from accounts import views as account_views

urlpatterns = [
    path("", account_views.home, name="home"),
    path("admin/", admin.site.urls),
    path("dashboard/", account_views.dashboard, name="dashboard"),
    path("login/", account_views.SkyLoginView.as_view(), name="login"),
    path("admin-login/", account_views.AdminLoginView.as_view(), name="admin_login"),
    path("logout/", account_views.sky_logout, name="logout"),
    path("signup/", account_views.signup, name="signup"),
    path("signup/success/", account_views.signup_success, name="signup_success"),
    path("redirecting/", account_views.redirecting, name="redirecting"),
    path("signed-out/", account_views.logged_out, name="logged_out"),
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/password_reset_email.html",
            success_url=reverse_lazy("password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    path("teams/", include("teams.urls")),
    path("meetings/", include("meetings.urls")),
    path("audit/", include("audit.urls")),
]
