from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Meeting(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    platform = models.CharField(max_length=100)
    message = models.TextField(blank=True)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "meeting"

    def __str__(self):
        return self.title
