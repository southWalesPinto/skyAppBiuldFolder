from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Conversation, Message

User = get_user_model()


class MessagingTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="adminSuper",
            password="adminSuper"
        )

        self.other_user = User.objects.create_user(
            username="user",
            password="Password123"
        )

        self.conversation = Conversation.objects.create()
        self.conversation.participants.add(self.user, self.other_user)

        self.message = Message.objects.create(
            conversation=self.conversation,
            sender=self.other_user,
            recipient=self.user,
            subject="Test Inbox Message",
            body="This is a test inbox message.",
            is_draft=False,
            sent_at=timezone.now()
        )

        self.draft = Message.objects.create(
            conversation=self.conversation,
            sender=self.user,
            recipient=self.other_user,
            subject="Draft Message",
            body="This is a draft message.",
            is_draft=True,
            sent_at=None
        )

    def test_inbox_page_shows_received_messages(self):
        self.client.login(username="adminSuper", password="adminSuper")
        response = self.client.get(reverse("messaging:inbox"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Inbox Message")

    def test_view_message_page_shows_full_message(self):
        self.client.login(username="adminSuper", password="adminSuper")
        response = self.client.get(
            reverse("messaging:view_message", args=[self.message.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This is a test inbox message.")

    def test_sent_page_loads(self):
        self.client.login(username="adminSuper", password="adminSuper")
        response = self.client.get(reverse("messaging:sent"))

        self.assertEqual(response.status_code, 200)

    def test_drafts_page_shows_draft(self):
        self.client.login(username="adminSuper", password="adminSuper")
        response = self.client.get(reverse("messaging:drafts"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Draft Message")

    def test_edit_draft_page_loads(self):
        self.client.login(username="adminSuper", password="adminSuper")
        response = self.client.get(
            reverse("messaging:edit_draft", args=[self.draft.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Draft Message")

    def test_send_message_valid(self):
        self.client.login(username="adminSuper", password="adminSuper")

        response = self.client.post(reverse("messaging:compose_message"), {
            "recipient": "user",
            "subject": "Hello",
            "body": "Hello test message"
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Message.objects.filter(subject="Hello").exists())

    def test_send_message_empty_recipient_invalid(self):
        self.client.login(username="adminSuper", password="adminSuper")

        response = self.client.post(reverse("messaging:compose_message"), {
            "recipient": "",
            "subject": "No recipient",
            "body": "This should fail"
        })

        self.assertEqual(response.status_code, 404)

    def test_delete_draft(self):
        self.client.login(username="adminSuper", password="adminSuper")

        response = self.client.get(
            reverse("messaging:delete_draft", args=[self.draft.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Message.objects.filter(id=self.draft.id).exists())