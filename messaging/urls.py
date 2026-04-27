from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('sent/', views.sent_messages, name='sent'),
    path('drafts/', views.drafts, name='drafts'),
    path('drafts/edit/<int:message_id>/', views.edit_draft, name='edit_draft'),
    path('message/<int:message_id>/', views.view_message, name='view_message'),
]
