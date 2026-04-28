from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import Conversation, Message

User = get_user_model()


@login_required
def inbox(request):
    messages = Message.objects.filter(
        recipient=request.user,
        is_draft=False
    ).order_by("-created_at")

    return render(request, "messaging/inbox.html", {
        "messages": messages
    })


@login_required
def sent_messages(request):
    messages = Message.objects.filter(
        sender=request.user,
        is_draft=False
    ).order_by("-created_at")

    return render(request, "messaging/sent.html", {
        "messages": messages
    })


@login_required
def drafts(request):
    messages = Message.objects.filter(
        sender=request.user,
        is_draft=True
    ).order_by("-created_at")

    return render(request, "messaging/drafts.html", {
        "messages": messages
    })


@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if message.recipient == request.user:
        message.is_read = True
        message.save()

    return render(request, "messaging/view_message.html", {
        "message": message
    })


@login_required
def compose_message(request):
    if request.method == "POST":
        recipient_username = request.POST.get("recipient")
        subject = request.POST.get("subject")
        body = request.POST.get("body")

        recipient = get_object_or_404(User, username=recipient_username)

        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, recipient)

        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            recipient=recipient,
            subject=subject,
            body=body,
            is_draft=False,
            sent_at=timezone.now()
        )

        return redirect("messaging:inbox")

    return render(request, "messaging/compose.html")


@login_required
def edit_draft(request, message_id):
    message = get_object_or_404(
        Message,
        id=message_id,
        sender=request.user,
        is_draft=True
    )

    if request.method == "POST":
        recipient_username = request.POST.get("recipient")
        subject = request.POST.get("subject")
        body = request.POST.get("body")

        recipient = get_object_or_404(User, username=recipient_username)

        message.recipient = recipient
        message.subject = subject
        message.body = body

        if "send" in request.POST:
            message.is_draft = False
            message.sent_at = timezone.now()

        message.save()

        if "send" in request.POST:
            return redirect("messaging:sent")

        return redirect("messaging:drafts")

    return render(request, "messaging/edit_draft.html", {
        "message": message
    })


@login_required
def delete_draft(request, message_id):
    message = get_object_or_404(
        Message,
        id=message_id,
        sender=request.user,
        is_draft=True
    )

    message.delete()

    return redirect("messaging:drafts")