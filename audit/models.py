from django.db import models


class AuditLog(models.Model):
    
    class Meta:
        db_table = "auditLog"

    def __str__(self) -> str:
        return self.aud_number