from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import AuditLog

User = get_user_model()


class AuditAdminDownloadTest(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="pass",
        )
        self.client = Client()
        self.client.force_login(self.admin)
        self.log1 = AuditLog.objects.create(action="test", details="Detail 1")
        self.log2 = AuditLog.objects.create(action="test2", details="Detail 2")

    def test_download_selected_audit_logs_action(self):
        url = reverse("admin:audit_auditlog_changelist")
        response = self.client.post(
            url,
            {
                "action": "download_selected_audit_logs",
                "_selected_action": [str(self.log1.pk), str(self.log2.pk)],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("aud_number,action,user,details,timestamp", response.content.decode())

    def test_download_single_audit_log_url(self):
        url = reverse("admin:audit_auditlog_download", args=[self.log1.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn(self.log1.aud_number, response.content.decode())
