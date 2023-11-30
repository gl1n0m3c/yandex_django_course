from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


__all__ = []


class StatusURLTests(TestCase):
    def test_about_page(self):
        response = Client().get(reverse("about:about"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
