from django.urls import path
from . import views

app_name = "meetings"

urlpatterns = [
    path('', views.meeting_list, name='meeting_list'),
    path('create/', views.create_meeting, name='create_meeting'),
    path('upcoming/', views.upcoming_meetings, name='upcoming_meetings'),
    path('weekly/', views.weekly_meetings, name='weekly_meetings'),
    path('monthly/', views.monthly_meetings, name='monthly_meetings'),
    path('delete/<int:id>/', views.delete_meeting, name='delete_meeting'),
]

