from re import findall

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail
from transliterate import translit


__all__ = []


def get_normalized_text(value: str):
    regex = r"[A-Яа-яA-Za-z0-9]+"
    worlds = findall(regex, value)
    return translit("".join(worlds).lower().replace("_", ""), "ru")


class NamePublishedIdBasedModel(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="название",
        help_text="Максимум 150 символов",
        unique=True,
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="опубликовано",
    )

    class Meta:
        abstract = True


class SlugNormalizationsBasedModel(NamePublishedIdBasedModel):
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text=(
            "Максимальная длина - 200 символов, уникальное "
            "значение рамках таблицы, только цифры, "
            "буквы латиницы и символы `-` и `_`"
        ),
        verbose_name="слаг",
    )

    normalization = models.CharField(
        max_length=150,
        verbose_name="нормализированное имя",
        editable=False,
        unique=True,
        null=True,
    )

    def clean(self):
        self.normalization = get_normalized_text(self.name)
        if (
            type(self)
            .objects.filter(normalization=self.normalization)
            .exclude(id=self.id)
            .count()
            > 0
        ):
            raise ValidationError("Уже есть такой элемент")

    def save(self, *args, **kwargs):
        self.normalization = get_normalized_text(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Images(models.Model):
    name = models.CharField(
        max_length=150,
        help_text="Максимальная длина названия - 150 символов",
        verbose_name="название",
        unique=True,
    )

    def get_image_300x300(self):
        return get_thumbnail(self.image, "300x300", quality=51)

    def get_image_600x600(self):
        return get_thumbnail(self.image, "300x300", quality=51)

    def display_image(self):
        if self.image:
            return mark_safe(
                f"<img src='{self.get_image_300x300().url}' width=50>",
            )
        return "Нет изображения"

    class Meta:
        abstract = True

    display_image.short_description = "превью"
    display_image.allow_tags = True
