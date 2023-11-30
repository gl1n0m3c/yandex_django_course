from django.test import Client, TestCase
from django.urls import reverse

from catalog.models import Category, MainImageModel, Tag


__all__ = []


class TestContext(TestCase):
    fixtures = [
        "fixtures/test.json",
    ]

    def test_in_context(self):
        response = Client().get(reverse("homepage:homepage"))
        self.assertIn("items", response.context)

    def test_count_el_context_hompage(self):
        response = Client().get(reverse("homepage:homepage"))
        items = response.context["items"]
        self.assertEqual(len(items), 1)

    def test_count_el_context_item_list(self):
        response = Client().get(reverse("homepage:homepage"))
        items = response.context["items"]
        self.assertEqual(len(items), 1)

    def test_type_of_items(self):
        response = Client().get(reverse("homepage:homepage"))
        item = response.context["items"][0]
        self.assertIsInstance(item.tags.all()[0], Tag)
        self.assertIsInstance(item.category, Category)
        self.assertIsInstance(item.main_image, MainImageModel)

    def test_db_fields_tag(self):
        response = Client().get(reverse("homepage:homepage"))
        item = response.context["items"][0]
        tag_keys = item.tags.all()[0].__dict__.keys()
        self.assertIn("id", tag_keys)
        self.assertIn("name", tag_keys)
        self.assertNotIn("is_published", tag_keys)
        self.assertNotIn("slug", tag_keys)
        self.assertNotIn("normalization", tag_keys)

    def test_db_fields_category(self):
        response = Client().get(reverse("homepage:homepage"))
        item = response.context["items"][0]
        category_keys = item.category.__dict__.keys()
        self.assertIn("id", category_keys)
        self.assertIn("name", category_keys)
        self.assertNotIn("weight", category_keys)
        self.assertNotIn("is_published", category_keys)
        self.assertNotIn("slug", category_keys)
        self.assertNotIn("normalization", category_keys)

    def test_db_fields_main_image(self):
        response = Client().get(reverse("homepage:homepage"))
        item = response.context["items"][0]
        main_image_keys = item.main_image.__dict__.keys()
        self.assertIn("id", main_image_keys)
        self.assertIn("name", main_image_keys)
        self.assertIn("image", main_image_keys)

    def test_prefetched_obj_homepage(self):
        response = Client().get(reverse("homepage:homepage"))

        items = response.context["items"]

        for item in items:
            obj = item.__dict__

            self.assertIn("_prefetched_objects_cache", obj)
            self.assertIn("tags", obj["_prefetched_objects_cache"])

            if len(obj["_prefetched_objects_cache"]["tags"]):
                for tag in obj["_prefetched_objects_cache"]["tags"]:
                    self.assertIsInstance(tag, Tag)
