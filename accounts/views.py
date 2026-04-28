
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
import json

from .forms import LoginForm, SignUpForm, ordered_team_queryset
from audit.models import AuditLog
from teams.models import Teams

from .forms import LoginForm, SignUpForm


def home(request):
    return render(request, 'home/home.html', {})


def dashboard(request):
    from django.db.models import Q
    
    # Get recent teams (teams the user is member of)
    recent_teams = []
    if hasattr(request.user, 'teammember_profile'):
        team = request.user.teammember_profile.team
        if team:
            recent_teams = [team]
    elif hasattr(request.user, 'teamlead_profile'):
        team = request.user.teamlead_profile.team
        if team:
            recent_teams = [team]
    elif hasattr(request.user, 'departmentmanager_profile'):
        team = request.user.departmentmanager_profile.team
        if team:
            recent_teams = [team]
    
    # If no team found, show random teams for demo
    if not recent_teams:
        recent_teams = Teams.objects.all()[:3]
    
    # Get recent activities (last 5 team-related audit logs)
    recent_activities = AuditLog.objects.filter(
        action__in=['team_created', 'team_updated', 'member_added', 'dependency_changed']
    ).order_by('-timestamp')[:5]
    
    # Format activities with icons and descriptions
    activity_icons = {
        'team_created': '✨',
        'team_updated': '📝',
        'member_added': '👥',
        'dependency_changed': '🔗',
        'login': '🔓',
        'logout': '🔒',
    }
    
    activities_formatted = []
    for activity in recent_activities:
        activity_dict = {
            'description': activity.details,
            'timestamp': activity.timestamp,
            'icon': activity_icons.get(activity.action, '📋'),
        }
        activities_formatted.append(activity_dict)
    
    context = {
        "active_nav": "dashboard",
        "recent_teams": recent_teams,
        "recent_activities": activities_formatted,
    }
    
    return render(request, "accounts/dashboard.html", context)


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

def view_profile(request):
    """Display user profile"""
    from django.contrib.auth.decorators import login_required
    from django.http import HttpResponse
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Ensure user has a profile
    profile, created = request.user.profile.__class__.objects.get_or_create(user=request.user)
    
    return render(request, "accounts/view_profile.html", {
        "active_nav": "profile",
    })


def edit_profile(request):
    """Edit user profile"""
    from django.contrib.auth.decorators import login_required
    
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Ensure user has a profile
    profile, created = request.user.profile.__class__.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Get form data
        role = request.POST.get('role', 'other')
        phone_number = request.POST.get('phone_number', '')
        department = request.POST.get('department', '')
        about = request.POST.get('about', '')
        skills_json = request.POST.get('skills_json', '[]')
        
        # Parse skills
        try:
            skills = json.loads(skills_json)
        except json.JSONDecodeError:
            skills = []
        
        # Update profile
        profile.role = role
        profile.phone_number = phone_number
        profile.department = department
        profile.about = about
        profile.skills = skills
        profile.save()
        
        AuditLog.objects.create(
            action='profile_updated',
            user=request.user,
            details=f"User {request.user.username} updated their profile"
        )
        
        return redirect('accounts:profile_view')
    
    return render(request, "accounts/edit_profile.html", {
        "active_nav": "profile",
    })
