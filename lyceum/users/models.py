from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django_cleanup.signals import cleanup_pre_delete
from sorl.thumbnail import delete, get_thumbnail


__all__ = []


class UserManager(models.Manager):
    def active(self):
        return (
            self.get_queryset()
            .filter(is_active=True)
            .only(f"{User.username.field.name}")
        )


class UserProxy(User):
    objects = UserManager()

    class Meta:
        proxy = True


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name="пользователь",
    )

    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name="дата рождения",
    )

    image = models.ImageField(
        upload_to="user_main_images",
        blank=True,
        null=True,
        verbose_name="аватарка",
    )

    coffe_count = models.PositiveIntegerField(
        default=0,
        verbose_name="количество сваренных чашек кофе",
    )

    def get_image_300x300(self):
        return get_thumbnail(self.image, "300x300", quality=51)

    def display_image(self):
        if self.image:
            return mark_safe(
                f"<img src='{self.get_image_300x300().url}' width=50>",
            )
        return "Нет изображения"

    class Meta:
        verbose_name = "Дополнительное поле"
        verbose_name_plural = "Дополнительные поля"


def sorl_delete(**kwargs):
    delete(kwargs["file"])


cleanup_pre_delete.connect(sorl_delete)
