from django.shortcuts import get_object_or_404, redirect, render

from .forms import MeetingForm
from .models import Meeting


def _schedule_context(form=None, open_create_modal=False):
    meetings = Meeting.objects.all()
    return {
        "meetings": meetings,
        "active_nav": "schedule",
        "form": form or MeetingForm(),
        "open_create_modal": open_create_modal,
    }


def meeting_list(request):
    return render(request, "meetings/schedule.html", _schedule_context())


def create_meeting(request):
    if request.method == "POST":
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            if request.user.is_authenticated:
                meeting.created_by = request.user
            if not meeting.title:
                meeting.title = "Scheduled Meeting"
            meeting.save()
            return redirect("meetings:meeting_list")
        return render(
            request,
            "meetings/schedule.html",
            _schedule_context(form=form, open_create_modal=True),
        )

    return render(
        request,
        "meetings/schedule.html",
        _schedule_context(open_create_modal=True),
    )


def upcoming_meetings(request):
    meetings = Meeting.objects.all()
    return render(request, "meetings/upcoming_meetings.html", {"meetings": meetings})


def weekly_meetings(request):
    meetings = Meeting.objects.all()
    return render(request, "meetings/weekly_meetings.html", {"meetings": meetings})


def monthly_meetings(request):
    meetings = Meeting.objects.all()
    return render(request, "meetings/monthly_meetings.html", {"meetings": meetings})


def delete_meeting(request, id):
    meeting = get_object_or_404(Meeting, id=id)
    meeting.delete()
    return redirect("meetings:meeting_list")
