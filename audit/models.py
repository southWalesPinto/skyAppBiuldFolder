from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class AuditLog(models.Model):
    id = models.CharField(max_length=100, unique=True, primary_key=True)
    object_id = models.CharField(max_length=100)
    object_repr = models.CharField(max_length=200)
    action_flag = models.CharField(max_length=100)
    change_message = models.TextField(blank=True)
    content_type = models.ForeignKey("contenttypes.ContentType", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "audit_log"
        ordering = ["-action_time"]

    def __str__(self) -> str:
        return self.id