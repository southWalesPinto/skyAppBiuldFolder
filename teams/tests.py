
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Teams


class TeamPagesTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='teamviewer',
            email='viewer@example.com',
            password='StrongPass123!',
        )
        self.team = Teams.objects.create(
            name='Frontend Development',
            lead_name='Alex Thompson',
            lead_role='Engineering Manager',
            lead_email='alex.thompson@sky.com',
            department='Global Apps Engineering',
            location='London, UK',
            summary='Customer-facing web applications and design system ownership.',
            members_count=12,
            active_projects=12,
            repositories_count=8,
            dependencies_count=5,
            contacts=[{'name': 'Alex Thompson', 'role': 'Engineering Manager', 'initials': 'AT'}],
            members=[{'name': 'Alex Thompson', 'role': 'Engineering Manager', 'group': 'engineer', 'email': 'alex@sky.com', 'phone': '+44 20 7123 4567', 'initials': 'AT', 'color': '#4f46e5'}],
            repositories=[{'name': 'sky-frontend-components', 'description': 'Core component library', 'tags': ['Frontend'], 'stars': 124, 'forks': 45, 'updated': 'Updated 2 days ago', 'icon': '⌘'}],
            dependencies=[{'name': 'UI/UX Design Team', 'type': 'Upstream', 'manager': 'Emily Chen', 'status': 'Active', 'color': '#5b45e7'}],
            quick_links=[{'label': 'Team Documentation', 'url': '#'}],
        )

    def test_slug_is_generated(self):
        self.assertEqual(self.team.slug, 'frontend-development')

    def test_teams_directory_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('teams:teams_page'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Team Directory')
        self.assertContains(response, 'Team Names')
        self.assertContains(response, 'Frontend Development')

    def test_team_profile_renders(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('teams:team_profile', kwargs={'slug': self.team.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Frontend Development')
        self.assertContains(response, 'Overview')
        self.assertContains(response, 'Members')
