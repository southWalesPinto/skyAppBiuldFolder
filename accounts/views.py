
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from teams.models import Teams

from .forms import LoginForm, SignUpForm


def home(request):
    return render(request, 'home/home.html', {})


def dashboard(request):
    return render(request, "accounts/dashboard.html", {"active_nav": "dashboard"})


class SkyLoginView(LoginView):
    form_class = LoginForm
    template_name = "accounts/login.html"

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
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("admin:index")


def signup(request):
    if request.user.is_authenticated:
        return redirect("redirecting")
    teams = Teams.objects.order_by("name")
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("signup_success")
    else:
        form = SignUpForm()
    return render(request, "accounts/signup.html", {"form": form, "teams": teams})


def signup_success(request):
    return render(request, "accounts/signup_success.html")


def redirecting(request):
    return render(request, "accounts/redirecting.html")


def logged_out(request):
    return render(request, "accounts/logged_out.html")


def sky_logout(request):
    logout(request)
    return redirect("logged_out")
