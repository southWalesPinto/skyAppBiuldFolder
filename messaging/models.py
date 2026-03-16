from django.conf import settings
from django.db import models


class Conversation(models.Model):
    
    class Meta:
        db_table = "conversation"



class Message(models.Model):
    class Meta:
        db_table = "message"
