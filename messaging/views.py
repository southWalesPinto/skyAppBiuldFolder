from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()


@login_required
def inbox(request):
    messages = Message.objects.filter(
        recipient=request.user,
        is_draft=False
    ).order_by('-sent_at')

    return render(request, 'messaging/inbox.html', {'messages': messages})


@login_required
def sent_messages(request):
    messages = Message.objects.filter(
        sender=request.user,
        is_draft=False
    ).order_by('-sent_at')

    return render(request, 'messaging/sent.html', {'messages': messages})


@login_required
def drafts(request):
    messages = Message.objects.filter(
        sender=request.user,
        is_draft=True
    ).order_by('-created_at')

    return render(request, 'messaging/drafts.html', {'messages': messages})


@login_required
def view_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    # Mark as read if the logged-in user is the recipient
    if message.recipient == request.user and not message.is_read:
        message.is_read = True
        message.save()

    return render(request, 'messaging/viewmessage.html', {'message': message})


@login_required
def edit_draft(request, message_id):
    message = get_object_or_404(
        Message,
        id=message_id,
        sender=request.user,
        is_draft=True
    )

    if request.method == 'POST':
        recipient_username = request.POST.get('recipient')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        send = request.POST.get('send')

        try:
            recipient = User.objects.get(username=recipient_username)
        except User.DoesNotExist:
            return render(request, 'messaging/edit-draft.html', {
                'message': message,
                'error': 'User not found'
            })

        message.recipient = recipient
        message.subject = subject
        message.body = body

        if send:
            message.is_draft = False
            message.sent_at = timezone.now()

        message.save()

        return redirect('messaging:inbox')  # important because of app_name

    return render(request, 'messaging/edit-draft.html', {'message': message})