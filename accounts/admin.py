from django.contrib import admin

from .models import DepartmentManager, TeamLead, TeamMember, User, UserProfile


admin.site.register(User)
admin.site.register(TeamMember)
admin.site.register(TeamLead)
admin.site.register(DepartmentManager)
admin.site.register(UserProfile)
