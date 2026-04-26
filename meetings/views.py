from django.shortcuts import render, redirect
from .models import Meeting
from .forms import MeetingForm


def meeting_list(request):
    meetings = Meeting.objects.all()
    return render(request, 'meetings/meeting_list.html', {'meetings': meetings})


def create_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('meetings:meeting_list')
    else:
        form = MeetingForm()

    return render(request, 'meetings/create_meeting.html', {'form': form})


def upcoming_meetings(request):
    meetings = Meeting.objects.all()
    return render(request, 'meetings/upcoming_meetings.html', {'meetings': meetings})


def weekly_meetings(request):
    meetings = Meeting.objects.all()
    return render(request, 'meetings/weekly_meetings.html', {'meetings': meetings})


def monthly_meetings(request):
    meetings = Meeting.objects.all()
    return render(request, 'meetings/monthly_meetings.html', {'meetings': meetings})

def delete_meeting(request, id):
    meeting = get_object_or_404(Meeting, id=id)
    meeting.delete()
    return redirect('meetings:meeting_list')

