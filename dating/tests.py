import os

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from dating.models import Invitation, Like, Photo

User = get_user_model()


@override_settings(MEDIA_ROOT="test_media")
class DatingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username="user1", password="pass12345")
        self.user2 = User.objects.create_user(username="user2", password="pass12345")
        self.client.login(username="user1", password="pass12345")

    def tearDown(self):
        if os.path.exists("test_media"):
            for root, dirs, files in os.walk("test_media", topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir("test_media")

    def test_photo_upload(self):
        import base64

        png_bytes = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
        )
        image = SimpleUploadedFile("test.png", png_bytes, content_type="image/png")
        url = reverse("photo-list")
        response = self.client.post(
            url, {"image": image, "is_main": True}, format="multipart"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Photo.objects.count(), 1)

    def test_like_creation(self):
        url = reverse("like-list")
        response = self.client.post(url, {"to_user": self.user2.id, "kind": "like"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Like.objects.count(), 1)

    def test_like_uniqueness(self):
        Like.objects.create(from_user=self.user1, to_user=self.user2, kind="like")
        url = reverse("like-list")
        response = self.client.post(url, {"to_user": self.user2.id, "kind": "like"})
        self.assertEqual(response.status_code, 400)

    def test_invitation_accept(self):
        invitation = Invitation.objects.create(from_user=self.user1, to_user=self.user2)
        url = reverse("invitation-accept", args=[invitation.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        invitation.refresh_from_db()
        self.assertEqual(invitation.status, "accepted")
