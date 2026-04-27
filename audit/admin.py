import csv
from urllib.parse import quote

from django.contrib import admin
from django.http import Http404, HttpResponse
from django.urls import path, reverse

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("aud_number", "action", "user", "timestamp")
    actions = ["download_selected_audit_logs"]
    change_form_template = "admin/audit/auditlog/change_form.html"

    def get_urls(self):
        urls = super().get_urls()

        custom_url = [
            path(
                "<path:object_id>/download/",
                self.download_single_audit_log,
                name="audit_auditlog_download",
            ),
        ]
        return custom_url + urls

    def download_selected_audit_logs(self, request, queryset):
        if queryset.exists():
            return self.build_csv_response(queryset, filename="audit_logs.csv")

        return None

    download_selected_audit_logs.short_description = "Download selected audit logs"

    def download_single_audit_log(self, request, object_id):
        obj = self.get_object(request, object_id)

        if obj is None:
            raise Http404("Audit log not found.")

        return self.build_csv_response([obj], filename=f"audit_log_{obj.aud_number}.csv")

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}

        extra_context["download_url"] = reverse(
            "admin:audit_auditlog_download",
            args=[quote(str(object_id))],
        )
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def build_csv_response(self, queryset, filename="audit_logs.csv"):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        writer = csv.writer(response)
        writer.writerow(["aud_number", "action", "user", "details", "timestamp"])
        
        for audit in queryset:
            writer.writerow([
                audit.aud_number,
                audit.action,
                str(audit.user) if audit.user else "",
                audit.details,
                audit.timestamp,
            ])
        return response
