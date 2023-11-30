from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


__all__ = []


class StatusURLTests(TestCase):
    def test_homepage_endpoint(self):
        response = Client().get(reverse("homepage:homepage"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_coffee(self):
        response = Client().get(reverse("homepage:coffee"))
        self.assertEqual("Я чайник".encode(), response.content)
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)

    def test_homepage_echo_get(self):
        response = Client().get(reverse("homepage:echo"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_homepage_echo_post(self):
        content = {
            "text": "test_text",
        }
        response = Client().post(reverse("homepage:echo"), content)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_homepage_echo_submit_get(self):
        response = Client().get(reverse("homepage:echo_submit"))
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_homepage_echo_submit_post(self):
        content = {
            "text": "test_text",
        }
        response = Client().post(reverse("homepage:echo_submit"), content)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.content, "test_text".encode("utf-8"))
