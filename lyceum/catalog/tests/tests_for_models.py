from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from parameterized import parameterized

from catalog.models import Category, Item, MainImageModel, Tag


__all__ = []


class TestModelCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category = Category.objects.create(
            is_published=True,
            name="Тестовое имя",
            slug="test-category-slug",
            weight=100,
        )

        cls.tag = Tag.objects.create(
            is_published=True,
            name="Тестовое имя",
            slug="test-tag-slug",
        )

        image_file = SimpleUploadedFile(
            "test_image.jpg",
            b"\x12\x34\x56\x78\x90\xAB\xCD\xEF",
            content_type="image/jpeg",
        )

        cls.main_image = MainImageModel.objects.create(
            name="test",
            image=image_file,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.main_image.image.delete()
        cls.main_image.delete()

    def test_tag_slug_simbols_wrong(self):
        tag_count = Tag.objects.count()
        tag = Tag(name="test_name", slug="!@#^&")
        with self.assertRaises(ValidationError):
            tag.full_clean()
            tag.save()
        self.assertEqual(tag_count, Tag.objects.count())

    def test_tag_slug_simbols_correct(self):
        tag_count = Tag.objects.count()
        tag = Tag(name="test_name", slug="correct_slug_name")
        tag.full_clean()
        tag.save()
        self.assertEqual(tag_count + 1, Tag.objects.count())

    def test_category_weight_wrong(self):
        category_count = Category.objects.count()
        category1 = Category(name="test_name1", slug="test_slug1", weight=0)
        category2 = Category(
            name="test_name2",
            slug="test_slug2",
            weight=32768,
        )
        with self.assertRaises(ValidationError):
            category1.full_clean()
            category1.save()
        with self.assertRaises(ValidationError):
            category2.full_clean()
            category2.save()
        self.assertEqual(category_count, Category.objects.count())

    def test_category_weight_correct(self):
        category_count = Category.objects.count()
        category = Category(
            name="Тестовое имяя",
            slug="test_slug2",
            weight=200,
        )
        category.full_clean()
        category.save()
        self.assertEqual(category_count + 1, Category.objects.count())

    def test_item_text_wrong(self):
        item_count = Item.objects.count()
        item = Item(
            name="test_name",
            category=self.category,
            text="Отвратительное название",
            main_image=self.main_image,
        )

        with self.assertRaises(ValidationError):
            item.full_clean()
            item.tags.add(self.tag)
            item.save()
        self.assertEqual(item_count, Item.objects.count())

    def test_item_text_correct(self):
        item_count = Item.objects.count()
        item = Item(
            name="test_name",
            category=self.category,
            text="Название превосходно",
            main_image=self.main_image,
        )
        item.full_clean()
        item.save()
        item.tags.add(self.tag)
        item.save()
        self.assertEqual(item_count + 1, Item.objects.count())

    @parameterized.expand(
        [
            "Тестовое имя!",
            "ТеСтоВое ИмЯ",
            "Тес-! тово!! е и-мя",
        ],
    )
    def test_unable_name_create_category(self, name):
        item_count = Category.objects.count()
        with self.assertRaises(ValidationError):
            category = Category(
                name=name,
                slug="TK-slag",
                weight=1,
            )
            category.full_clean()
            category.save()

        self.assertEqual(Category.objects.count(), item_count)
