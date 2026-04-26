
from django.shortcuts import get_object_or_404, render

from .models import Teams


def teams_page(request):
    teams = Teams.objects.all()
    return render(
        request,
        "teams.html",
        {
            "teams": teams,
            "active_nav": "teams",
        },
    )


def team_profile(request, slug):
    team = get_object_or_404(Teams, slug=slug)
    return render(
        request,
        "team_profile.html",
        {
            "team": team,
            "active_nav": "teams",
        },
    )
