from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


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
