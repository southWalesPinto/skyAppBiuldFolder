from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AuditLog(models.Model):
    aud_number = models.CharField(max_length=100, unique=True)
    action = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "auditLog"
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        return self.aud_number