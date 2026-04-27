
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import LoginForm, SignUpForm, ordered_team_queryset
from audit.models import AuditLog
from teams.models import Teams

from .forms import LoginForm, SignUpForm


def home(request):
    return render(request, 'home/home.html', {})


def dashboard(request):
    return render(request, "accounts/dashboard.html", {"active_nav": "dashboard"})


class SkyLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        AuditLog.objects.create(
            action="login",
            user=self.request.user,
            details=f"User {self.request.user.username} logged in at {timezone.now()}"
        )
        return response

    def get_success_url(self):
        return reverse_lazy("dashboard")


class AdminLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/admin_login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        if not form.get_user().is_staff:
            form.add_error(None, "This login page is for admin users only.")
            return self.form_invalid(form)
        response = super().form_valid(form)
        AuditLog.objects.create(
            action="admin_login",
            user=self.request.user,
            details=f"Admin {self.request.user.username} logged in at {timezone.now()}"
        )
        return response

    def get_success_url(self):
        return reverse_lazy("admin:index")


def signup(request):
    if request.user.is_authenticated:
        return redirect("redirecting")
    teams = ordered_team_queryset()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            AuditLog.objects.create(
                action="signup",
                user=user,
                details=f"User {user.username} signed up at {timezone.now()}"
            )
            login(request, user)
            return redirect("signup_success")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form, "teams": teams})


def signup_success(request):
    return redirect("login")


def redirecting(request):
    return render(request, "accounts/redirecting.html")


def logged_out(request):
    return render(request, "accounts/logged_out.html")


def sky_logout(request):
    user = request.user
    logout(request)
    AuditLog.objects.create(
        action="logout",
        user=user,
        details=f"User {user.username} logged out at {timezone.now()}"
    )
    return redirect("logged_out")
