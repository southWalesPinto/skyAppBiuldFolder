from django.db import models


class Project(models.Model):

    class Meta:
        db_table = "project"

    def __str__(self) -> str:
        return self.proj_name




