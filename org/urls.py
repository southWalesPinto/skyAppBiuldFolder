from django.urls import path

from . import views

app_name = "org"

urlpatterns = [
    path("", views.organisation_page, name="organisation_page"),
]
