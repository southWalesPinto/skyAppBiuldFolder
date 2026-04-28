import uuid

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Case, IntegerField, Value, When

from teams.models import Teams

from .models import DepartmentManager, TeamLead, TeamMember, UserProfile

User = get_user_model()


TEAM_DIAGRAM_ORDER = [
    "Core Team",
    "Mobile",
    "Team Gamma",
    "Team Zeta",
    "Team Epsilon",
    "Team Theta",
    "Team Delta",
    "Team Beta",
    "Team Alpha",
    "Backend Team",
    "Security Team",
    "Frontend Team",
]


def ordered_team_queryset():
    order_case = Case(
        *[When(name=name, then=Value(index)) for index, name in enumerate(TEAM_DIAGRAM_ORDER)],
        default=Value(len(TEAM_DIAGRAM_ORDER)),
        output_field=IntegerField(),
    )
    return Teams.objects.annotate(_team_order=order_case).order_by("_team_order", "name")


class SignUpForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ("team_member", "Team Member"),
        ("team_lead", "Team Lead"),
        ("department_manager", "Department Manager"),
    ]

    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Full name"}))
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
    team = forms.ModelChoiceField(queryset=Teams.objects.none(), required=True, empty_label="Choose a team")
    phone_number = forms.CharField(required=False, max_length=30)
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))

    class Meta:
        model = User
        fields = ("username", "name", "team", "user_type", "phone_number", "notes", "password1", "password2")
        widgets = {
            "username": forms.EmailInput(attrs={"placeholder": "Email address"}),
            "team": forms.Select(attrs={"data-team-select": "true"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["team"].queryset = ordered_team_queryset()
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm password"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Phone number (optional)"
        self.fields["notes"].widget.attrs["placeholder"] = "Notes (optional)"

    def _new_code(self, prefix: str) -> str:
        return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"

    def save(self, commit=True):
        if not commit:
            raise ValueError("SignUpForm.save requires commit=True")

        user = super().save(commit=True)
        user.first_name = self.cleaned_data.get("name", "")
        user.save(update_fields=["first_name"])

        user_type = self.cleaned_data["user_type"]
        team = self.cleaned_data["team"]
        phone_number = self.cleaned_data.get("phone_number", "")
        notes = self.cleaned_data.get("notes", "")

        if user_type == "team_member":
            TeamMember.objects.create(
                user=user,
                team=team,
                member_code=self._new_code("TM"),
                phone_number=phone_number,
                notes=notes,
            )
        elif user_type == "team_lead":
            TeamLead.objects.create(
                user=user,
                team=team,
                lead_code=self._new_code("TL"),
                phone_number=phone_number,
                notes=notes,
            )
        else:
            DepartmentManager.objects.create(
                user=user,
                team=team,
                manager_code=self._new_code("DM"),
                phone_number=phone_number,
                notes=notes,
            )

        # Create UserProfile
        profile_role = 'other'
        if user_type == 'team_member':
            profile_role = 'frontend_developer'
        elif user_type == 'team_lead':
            profile_role = 'team_lead'
        elif user_type == 'department_manager':
            profile_role = 'manager'

        UserProfile.objects.create(
            user=user,
            role=profile_role,
            department=team.name if team else '',
            about=notes or '',
        )

        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Email / Username"
        self.fields["password"].widget.attrs["placeholder"] = "Password"
