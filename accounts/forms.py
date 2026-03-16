import uuid

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import DepartmentManager, TeamLead, TeamMember

User = get_user_model()


class SignUpForm(UserCreationForm):
    USER_TYPE_CHOICES = [
        ("team_member", "Team Member"),
        ("team_lead", "Team Lead"),
        ("department_manager", "Department Manager"),
    ]

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder": "Email address"}))
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
    phone_number = forms.CharField(required=False, max_length=30)
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))

    class Meta:
        model = User
        fields = ("username", "email", "user_type", "phone_number", "notes", "password1", "password2")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Full name / username"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        user_type = self.cleaned_data["user_type"]
        phone_number = self.cleaned_data.get("phone_number", "")
        notes = self.cleaned_data.get("notes", "")

        if user_type == "team_member":
            TeamMember.objects.create(
                user=user,
                member_code=self._new_code("TM"),
                phone_number=phone_number,
                notes=notes,
            )
        elif user_type == "team_lead":
            TeamLead.objects.create(
                user=user,
                lead_code=self._new_code("TL"),
                phone_number=phone_number,
                notes=notes,
            )
        else:
            DepartmentManager.objects.create(
                user=user,
                manager_code=self._new_code("DM"),
                phone_number=phone_number,
                notes=notes,
            )

        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Email / Username"
        self.fields["password"].widget.attrs["placeholder"] = "Password"
