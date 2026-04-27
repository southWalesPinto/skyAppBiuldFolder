from django.conf import settings
from django.db import models
from django.conf import settings


class Meeting(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    platform = models.CharField(max_length=100, null=True, blank=True)
    message = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "meeting"

    def __str__(self):
        return self.title
