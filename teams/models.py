
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Teams(models.Model):
    STATUS_ACTIVE = "active"
    STATUS_PAUSED = "paused"
    STATUS_ARCHIVED = "archived"

    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_PAUSED, "Paused"),
        (STATUS_ARCHIVED, "Archived"),
    ]

    name = models.CharField(max_length=120, default="New Team")
    slug = models.SlugField(max_length=140, unique=True, null=True, blank=True)
    lead_name = models.CharField(max_length=120, default="Team Lead")
    lead_role = models.CharField(max_length=120, default="Team Lead")
    lead_email = models.EmailField(default="team@sky.com")
    department = models.CharField(max_length=120, default="General")
    location = models.CharField(max_length=120, default="Remote")
    summary = models.TextField(blank=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    members_count = models.PositiveIntegerField(default=0)
    active_projects = models.PositiveIntegerField(default=0)
    repositories_count = models.PositiveIntegerField(default=0)
    dependencies_count = models.PositiveIntegerField(default=0)
    banner_start = models.CharField(max_length=20, default="#d8e6ff")
    banner_end = models.CharField(max_length=20, default="#c2d7ff")
    accent_color = models.CharField(max_length=20, default="#5b45e7")
    accent_soft_color = models.CharField(max_length=20, default="#f3efff")
    profile_gradient_start = models.CharField(max_length=20, default="#5a18e6")
    profile_gradient_end = models.CharField(max_length=20, default="#2d6ef2")
    contacts = models.JSONField(default=list, blank=True)
    members = models.JSONField(default=list, blank=True)
    repositories = models.JSONField(default=list, blank=True)
    dependencies = models.JSONField(default=list, blank=True)
    quick_links = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = "teams"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "team"
            slug = base_slug
            suffix = 2
            existing = Teams.objects.all()
            if self.pk:
                existing = existing.exclude(pk=self.pk)
            while existing.filter(slug=slug).exists():
                slug = f"{base_slug}-{suffix}"
                suffix += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("teams:team_profile", kwargs={"slug": self.slug})

    @property
    def initials(self) -> str:
        pieces = [part[0] for part in self.name.split() if part]
        if not pieces:
            return "T"
        return "".join(pieces[:2]).upper()

    @property
    def status_label(self) -> str:
        return self.get_status_display()
