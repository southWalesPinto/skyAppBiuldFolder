from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from teams.models import Teams


class User(AbstractUser):
    """Primary auth user model for the project."""

    def __str__(self) -> str:
        return self.username


class AbstractUserType(models.Model):
    """Abstract base for concrete user-type records."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_profile",
    )
    team = models.ForeignKey(
        Teams,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_team_members",
    )
    phone_number = models.CharField(max_length=30, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class TeamMember(AbstractUserType):
    member_code = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "team_member"

    def __str__(self) -> str:
        return f"TeamMember<{self.user.username}>"


class TeamLead(AbstractUserType):
    lead_code = models.CharField(max_length=50, unique=True)
    can_approve_tasks = models.BooleanField(default=True)

    class Meta:
        db_table = "team_lead"

    def __str__(self) -> str:
        return f"TeamLead<{self.user.username}>"


class DepartmentManager(AbstractUserType):
    manager_code = models.CharField(max_length=50, unique=True)
    can_manage_departments = models.BooleanField(default=True)

    class Meta:
        db_table = "department_manager"

    def __str__(self) -> str:
        return f"DepartmentManager<{self.user.username}>"

class UserProfile(models.Model):
    """Extended user profile with skills, about, and display info."""
    
    ROLE_CHOICES = (
        ('frontend_developer', 'Frontend Developer'),
        ('backend_developer', 'Backend Developer'),
        ('full_stack_developer', 'Full Stack Developer'),
        ('devops_engineer', 'DevOps Engineer'),
        ('qa_engineer', 'QA Engineer'),
        ('product_manager', 'Product Manager'),
        ('team_lead', 'Team Lead'),
        ('manager', 'Manager'),
        ('other', 'Other'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default='other')
    department = models.CharField(max_length=150, blank=True)
    about = models.TextField(blank=True, help_text="Professional bio and background")
    skills = models.JSONField(default=list, blank=True, help_text="List of technical skills")
    avatar_gradient_start = models.CharField(
        max_length=7, 
        default='#4B5BE5',
        help_text="Hex color for avatar gradient start"
    )
    avatar_gradient_end = models.CharField(
        max_length=7, 
        default='#7B68EE',
        help_text="Hex color for avatar gradient end"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profile'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self) -> str:
        return f"Profile<{self.user.username}>"
    
    def get_initials(self) -> str:
        first = self.user.first_name[0] if self.user.first_name else ''
        last = self.user.last_name[0] if self.user.last_name else ''
        return (first + last).upper() or self.user.username[0].upper()
    
    def get_role_display_name(self) -> str:
        return dict(self.ROLE_CHOICES).get(self.role, self.role)
