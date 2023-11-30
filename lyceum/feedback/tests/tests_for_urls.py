from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


__all__ = []


class UrlTests(TestCase):
    def test_feedback_url_get(self):
        response = Client().get(reverse("feedback:feedback"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_feedback_url_post_redirect(self):
        content = {
            "name": "test",
            "text": "test_text",
            "mail": "example@example.com",
        }

        response = Client().post(
            reverse("feedback:feedback"),
            content,
            follow=True,
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse("feedback:feedback"))
