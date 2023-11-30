from datetime import timedelta

from ckeditor.fields import RichTextField
from django.core import validators
from django.db import models
from django.utils import timezone
from django_cleanup.signals import cleanup_pre_delete
from sorl.thumbnail import delete

from catalog.validators import ValidateMustContain
from core.models import (
    Images,
    NamePublishedIdBasedModel,
    SlugNormalizationsBasedModel,
)


__all__ = []


class ItemManager(models.Manager):
    def published(self):
        return (
            self.get_queryset()
            .select_related(Item.category.field.name)
            .filter(
                is_published=True,
                category__is_published=True,
            )
            .prefetch_related(
                models.Prefetch(
                    Item.tags.field._related_query_name,
                    queryset=Tag.objects.filter(is_published=True).only(
                        Tag.name.field.name,
                    ),
                ),
            )
            .only(
                Item.name.field.name,
                Item.text.field.name,
                f"{Item.category.field.name}__{Category.name.field.name}",
            )
        )

    def get_item_list_page(self):
        return self.published().order_by(
            Item.category.field.name,
            Item.name.field.name,
        )

    def on_main(self):
        return self.published().filter(is_on_main=True)

    def get_item(self):
        return (
            self.get_queryset()
            .select_related(
                Item.category.field.name,
                Item.main_image.field.name,
            )
            .filter(
                is_published=True,
                category__is_published=True,
            )
            .prefetch_related(
                models.Prefetch(
                    Item.tags.field._related_query_name,
                    queryset=Tag.objects.filter(is_published=True).only(
                        Tag.name.field.name,
                    ),
                ),
                models.Prefetch(
                    Item.images.field._related_name,
                    queryset=ManyImageModel.objects.only(
                        ManyImageModel.image.field.name,
                        ManyImageModel.item.field.name,
                    ),
                ),
            )
            .only(
                Item.name.field.name,
                Item.text.field.name,
                f"{Item.category.field.name}__{Category.name.field.name}",
                Item.main_image.field.name,
            )
        )

    def get_new(self):
        items = (
            self.published()
            .filter(
                created__gte=(timezone.now() - timezone.timedelta(days=7)),
            )
            .order_by(Item.category.field.name, "?")
        )
        return items[:5]

    def get_fridays(self):
        items = (
            self.published()
            .filter(updated__week_day=6)
            .order_by(Item.created.field.name, Item.category.field.name)
        )
        return items[:5]

    def get_unverified(self):
        return (
            self.published()
            .filter(
                created__gte=models.F(Item.updated.field.name) - timedelta(seconds=1),
            )
            .filter(
                created__lte=models.F(Item.updated.field.name) + timedelta(seconds=1),
            )
            .order_by(Item.category.field.name)
        )


class MainImageModel(Images):
    image = models.ImageField(
        upload_to="main_images",
        verbose_name="изображение",
    )

    class Meta:
        verbose_name = "главное изображение"
        verbose_name_plural = "главные изображения"

    def __str__(self):
        return self.name


class Tag(SlugNormalizationsBasedModel):
    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"

    def __str__(self):
        return self.name


class Category(SlugNormalizationsBasedModel):
    weight = models.IntegerField(
        default=100,
        validators=[
            validators.MinValueValidator(1),
            validators.MaxValueValidator(32767),
        ],
        verbose_name="Вес",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name


class Item(NamePublishedIdBasedModel):
    objects = ItemManager()

    is_on_main = models.BooleanField(
        default=False,
        verbose_name="опубликовано на главной",
    )

    main_image = models.OneToOneField(
        MainImageModel,
        on_delete=models.CASCADE,
        help_text="Выберите главное изображение товара",
        verbose_name="главное изображение",
        related_name="items",
        related_query_name="main_image",
        null=True,
        blank=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        verbose_name="категория",
        help_text="Выберите категорию",
        related_name="items",
        related_query_name="category",
    )

    tags = models.ManyToManyField(
        Tag,
        help_text="Выберите теги, описывающие данный товар.",
        related_name="items",
        related_query_name="tags",
    )

    text = RichTextField(
        validators=[ValidateMustContain("превосходно", "роскошно")],
        verbose_name="Описание",
        help_text=(
            "Добавьте краткое описание товара используя "
            "слова `превосходно` или `роскошно`"
        ),
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата создания",
        null=True,
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="дата обновления",
        null=True,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return self.name


class ManyImageModel(Images):
    image = models.ImageField(
        upload_to="extra_images",
        verbose_name="изображение",
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="images",
        related_query_name="items",
    )

    class Meta:
        verbose_name = "изображение"
        verbose_name_plural = "изображения"

    def __str__(self):
        return self.name


def sorl_delete(**kwargs):
    delete(kwargs["file"])


cleanup_pre_delete.connect(sorl_delete)
