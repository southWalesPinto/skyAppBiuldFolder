import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class AuditLog(models.Model):
    aud_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    action = models.CharField(max_length=100, default="created")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = "auditLog"
        ordering = ["-timestamp"]

    def save(self, *args, **kwargs):
        if not self.aud_number:
            self.aud_number = f"AUD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.aud_number or f"AuditLog#{self.pk}"