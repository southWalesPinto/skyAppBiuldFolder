from django.core.exceptions import ValidationError
from django.db import models


class Department(models.Model):

    class Meta:
        db_table = "department"

    def __str__(self) -> str:
        return self.dep_name
