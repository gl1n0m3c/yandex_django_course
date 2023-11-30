from http import HTTPStatus
import re

from django.test import Client, TestCase
from django.test.utils import override_settings
from django.urls import reverse


__all__ = []


RUSSIAN_WORDS_REGULAR = re.compile(r"[а-яА-Я]+")


class MiddlewareTests(TestCase):
    @override_settings(ALLOW_REVERSE=True)
    def test_middleware_reverse_true(self):
        answers = set()
        for _ in range(10):
            response = Client().get(reverse("homepage:coffee"))
            words = RUSSIAN_WORDS_REGULAR.findall(
                response.content.decode("UTF-8"),
            )
            answers.add(words[0])
            answers.add(words[1])
            self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
        self.assertIn("Я", answers)
        self.assertIn("чайник", answers)
        self.assertIn("кинйач", answers)
        self.assertEqual(len(answers), 3)

    @override_settings(ALLOW_REVERSE=False)
    def test_middleware_reverse_false(self):
        answers = set()
        for _ in range(10):
            response = Client().get(reverse("homepage:coffee"))
            words = RUSSIAN_WORDS_REGULAR.findall(
                response.content.decode("UTF-8"),
            )
            answers.add(words[0])
            answers.add(words[1])
            self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
        self.assertIn("Я", answers)
        self.assertIn("чайник", answers)
        self.assertEqual(len(answers), 2)
