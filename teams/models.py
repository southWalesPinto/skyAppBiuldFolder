from django.db import models

class Teams(models.Model):

    class Meta:
        db_table = "teams"

    def __str__(self) -> str:
        return self.tea_name
