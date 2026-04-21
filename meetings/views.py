from datetime import timedelta
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Meeting
from .forms import MeetingForm


@login_required
def meeting_list(request):
    meetings = Meeting.objects.all().order_by('date', 'time')
    return render(request, 'meetings/meeting_list.html', {'meetings': meetings})


@login_required
def create_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.created_by = request.user
            meeting.save()
            return redirect('meetings:meeting_list')
    else:
        form = MeetingForm()

    return render(request, 'meetings/create_meeting.html', {'form': form})


@login_required
def upcoming_meetings(request):
    today = timezone.now().date()
    meetings = Meeting.objects.filter(date__gte=today).order_by('date', 'time')
    return render(request, 'meetings/upcoming_meetings.html', {'meetings': meetings})


@login_required
def weekly_meetings(request):
    today = timezone.now().date()
    end_date = today + timedelta(days=7)
    meetings = Meeting.objects.filter(date__range=[today, end_date])
    return render(request, 'meetings/weekly_meetings.html', {'meetings': meetings})


@login_required
def monthly_meetings(request):
    today = timezone.now().date()
    end_date = today + timedelta(days=30)
    meetings = Meeting.objects.filter(date__range=[today, end_date])
    return render(request, 'meetings/monthly_meetings.html', {'meetings': meetings})

