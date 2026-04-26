
from django.contrib import admin

from .models import Teams


@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    list_display = ("name", "lead_name", "department", "location", "status", "members_count")
    list_filter = ("status", "department", "location")
    search_fields = ("name", "lead_name", "department", "location")
    prepopulated_fields = {"slug": ("name",)}
