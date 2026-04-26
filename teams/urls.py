
from django.urls import path

from . import views

app_name = "teams"

urlpatterns = [
    path("", views.teams_page, name="teams_page"),
    path("<slug:slug>/", views.team_profile, name="team_profile"),
]
