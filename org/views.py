from django.shortcuts import render

from teams.models import Teams


def organisation_page(request):
    teams = list(Teams.objects.order_by("name"))
    total_members = sum(team.members_count or 0 for team in teams)
    return render(
        request,
        "org/organisation_page.html",
        {
            "teams": teams,
            "total_members": total_members,
            "active_nav": "organisation",
        },
    )
