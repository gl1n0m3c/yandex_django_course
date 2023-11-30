from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import NoReverseMatch, reverse
import parameterized


__all__ = []


class NameURLTests(TestCase):
    @parameterized.parameterized.expand([(0, 404), (123, 404)])
    def test_name_item_detail_correct(self, value, st):
        response = Client().get(reverse("catalog:item_detail", args=[value]))
        self.assertEqual(response.status_code, st)

    @parameterized.parameterized.expand(
        [-123, "asd", "1e5", "0.5", "@#&^$", "0asd", "asd0"],
    )
    def test_name_item_detail_incorrect(self, value):
        with self.assertRaises(NoReverseMatch):
            Client().get(reverse("catalog:item_detail", args=[value]))

    @parameterized.parameterized.expand(
        [
            "catalog:new",
            "catalog:friday",
            "catalog:unverified",
        ],
    )
    def test_new_friday_unverified_endpoints(self, url):
        response = Client().get(reverse(url))
        self.assertEqual(response.status_code, HTTPStatus.OK)
