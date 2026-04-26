from django.shortcuts import render
from .models import AuditLog

# Create your views here.
def AuditLogView(request):
    logs = AuditLog.objects.all()
    return render(request, "audit/report.html", {"logs": logs})