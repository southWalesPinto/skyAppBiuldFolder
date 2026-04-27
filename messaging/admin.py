from django.contrib import admin
from .models import Conversation, Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'is_draft', 'is_read', 'created_at')
    list_filter = ('is_draft', 'is_read')
    search_fields = ('subject', 'body')
    ordering = ('-created_at',)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at')
    filter_horizontal = ('participants',)