from django.urls import path

from . import views

app_name = "audit"


urlpatterns = [
    path("report/", views.AuditLogView, name="report"),

    ## For testing purposes
    path("test/", views.BaseView, name="base"),
]