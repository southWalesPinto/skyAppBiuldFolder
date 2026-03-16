from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import DepartmentManager, TeamLead, TeamMember


class SignUpUserTypeTests(TestCase):
    def _signup(self, user_type: str, username: str, email: str):
        return self.client.post(
            reverse("accounts:signup"),
            {
                "username": username,
                "email": email,
                "user_type": user_type,
                "phone_number": "123456789",
                "notes": "test note",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

    def test_signup_creates_team_member_profile(self):
        response = self._signup("team_member", "member_user", "member@example.com")

        self.assertRedirects(response, reverse("accounts:signup_success"))
        user = get_user_model().objects.get(username="member_user")

        self.assertTrue(TeamMember.objects.filter(user=user).exists())
        self.assertFalse(TeamLead.objects.filter(user=user).exists())
        self.assertFalse(DepartmentManager.objects.filter(user=user).exists())
        self.assertTrue(TeamMember.objects.get(user=user).member_code.startswith("TM-"))

    def test_signup_creates_team_lead_profile(self):
        response = self._signup("team_lead", "lead_user", "lead@example.com")

        self.assertRedirects(response, reverse("accounts:signup_success"))
        user = get_user_model().objects.get(username="lead_user")

        self.assertTrue(TeamLead.objects.filter(user=user).exists())
        self.assertFalse(TeamMember.objects.filter(user=user).exists())
        self.assertFalse(DepartmentManager.objects.filter(user=user).exists())
        self.assertTrue(TeamLead.objects.get(user=user).lead_code.startswith("TL-"))

    def test_signup_creates_department_manager_profile(self):
        response = self._signup("department_manager", "manager_user", "manager@example.com")

        self.assertRedirects(response, reverse("accounts:signup_success"))
        user = get_user_model().objects.get(username="manager_user")

        self.assertTrue(DepartmentManager.objects.filter(user=user).exists())
        self.assertFalse(TeamMember.objects.filter(user=user).exists())
        self.assertFalse(TeamLead.objects.filter(user=user).exists())
        self.assertTrue(DepartmentManager.objects.get(user=user).manager_code.startswith("DM-"))
