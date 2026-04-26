from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from teams.models import Teams

from .models import DepartmentManager, TeamLead, TeamMember


class SignUpUserTypeTests(TestCase):
    def _signup(self, user_type: str, username: str, email: str, team_id: int):
        response = self.client.post(
            reverse("signup"),
            {
                "username": username,
                "name": "Test User",
                "email": email,
                "user_type": user_type,
                "team": team_id,
                "phone_number": "123456789",
                "notes": "test note",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
            follow=True,
        )
        return response

    def setUp(self):
        self.team = Teams.objects.create(name="Frontend Development")

    def test_signup_creates_team_member_profile(self):
        response = self._signup("team_member", "member_user", "member@example.com", self.team.pk)

        self.assertRedirects(response, reverse("signup_success"))
        user = get_user_model().objects.get(username="member_user")

        self.assertTrue(TeamMember.objects.filter(user=user).exists())
        self.assertFalse(TeamLead.objects.filter(user=user).exists())
        self.assertFalse(DepartmentManager.objects.filter(user=user).exists())
        self.assertTrue(TeamMember.objects.get(user=user).member_code.startswith("TM-"))
        self.assertEqual(TeamMember.objects.get(user=user).team, self.team)

    def test_signup_creates_team_lead_profile(self):
        response = self._signup("team_lead", "lead_user", "lead@example.com", self.team.pk)

        self.assertRedirects(response, reverse("signup_success"))
        user = get_user_model().objects.get(username="lead_user")

        self.assertTrue(TeamLead.objects.filter(user=user).exists())
        self.assertFalse(TeamMember.objects.filter(user=user).exists())
        self.assertFalse(DepartmentManager.objects.filter(user=user).exists())
        self.assertTrue(TeamLead.objects.get(user=user).lead_code.startswith("TL-"))
        self.assertEqual(TeamLead.objects.get(user=user).team, self.team)

    def test_signup_creates_department_manager_profile(self):
        response = self._signup("department_manager", "manager_user", "manager@example.com", self.team.pk)

        self.assertRedirects(response, reverse("signup_success"))
        user = get_user_model().objects.get(username="manager_user")

        self.assertTrue(DepartmentManager.objects.filter(user=user).exists())
        self.assertFalse(TeamMember.objects.filter(user=user).exists())
        self.assertFalse(TeamLead.objects.filter(user=user).exists())
        self.assertTrue(DepartmentManager.objects.get(user=user).manager_code.startswith("DM-"))
        self.assertEqual(DepartmentManager.objects.get(user=user).team, self.team)



class AnonymousRedirectTests(TestCase):
    def test_protected_pages_redirect_to_login(self):
        protected_paths = [
            reverse("home"),
            reverse("dashboard"),
            reverse("teams:teams_page"),
            reverse("meetings:meeting_list"),
            reverse("audit:report"),
        ]

        for path in protected_paths:
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("login")))
