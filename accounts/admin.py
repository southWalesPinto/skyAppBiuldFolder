from django.contrib import admin

from .models import DepartmentManager, TeamLead, TeamMember, User


admin.site.register(User)
admin.site.register(TeamMember)
admin.site.register(TeamLead)
admin.site.register(DepartmentManager)
