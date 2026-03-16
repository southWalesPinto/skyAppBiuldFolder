from django.conf import settings
from django.db import models


class Meeting(models.Model):
    
    class Meta:
        db_table = "meeting"



class MeetingParticipant(models.Model):
    
    class Meta:
        db_table = "meeting_participant"

