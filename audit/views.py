from django.shortcuts import render
from .models import AuditLog

# Create your views here.
def AuditLogView(request):
    logs = AuditLog.objects.all()
    return render(request, 'report.html', {'logs': logs})

## For testing purposes
def BaseView(request):
    return render(request, 'base.html')