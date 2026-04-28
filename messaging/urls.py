from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path("inbox/", views.inbox, name="inbox"),
    path("sent/", views.sent_messages, name="sent"),
    path("drafts/", views.drafts, name="drafts"),
    path("message/<int:message_id>/", views.view_message, name="view_message"),
    path("compose/", views.compose_message, name="compose_message"),
    path("draft/<int:message_id>/edit/", views.edit_draft, name="edit_draft"),
    path("draft/<int:message_id>/delete/", views.delete_draft, name="delete_draft"),
]