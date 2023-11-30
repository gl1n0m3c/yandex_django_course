from pathlib import Path

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from sorl.thumbnail import delete


__all__ = []


STATUS_CHOICES = [
    ("received", "Получено"),
    ("processing", "В обработке"),
    ("answered", "Ответ дан"),
]


class Feedback(models.Model):
    text = models.TextField(verbose_name="текст")

    created_on = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name="дата создания",
    )

    status = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        default="received",
        verbose_name="статус",
    )

    class Meta:
        verbose_name = "обратная связь"
        verbose_name_plural = "обратные связи"

    def __str__(self):
        return f"{self.created_on}"


class PersonalData(models.Model):
    feedback = models.OneToOneField(
        Feedback,
        on_delete=models.CASCADE,
        verbose_name="фидбек",
    )

    name = models.TextField(
        verbose_name="имя",
        null=True,
        blank=True,
    )

    mail = models.EmailField(verbose_name="почта")

    class Meta:
        verbose_name = "персональные данные"
        verbose_name_plural = "персональные данные"

    def __str__(self):
        return self.name


class StatusLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="пользователь",
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="время",
    )

    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        verbose_name="фидбек",
    )

    from_status = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        verbose_name="из",
        db_column="from",
    )

    to = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        verbose_name="в",
    )

    class Meta:
        verbose_name = "лог"
        verbose_name_plural = "логи"

    def __str__(self):
        return self.user.first_name


class FileUpload(models.Model):
    def _feedback_upload_path(self, filename):
        return f"uploads/{self.feedback_id}/{filename}"

    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        related_name="uploads",
        verbose_name="фидбек",
    )

    file = models.FileField(
        upload_to=_feedback_upload_path,
        verbose_name="файлы",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "файл"
        verbose_name_plural = "файлы"

    def __str__(self):
        return str(self.feedback)


@receiver(pre_delete, sender=FileUpload)
def sorl_delete(sender, instance, **kwargs):
    delete(instance.file)

    folder_path = Path(instance.file.path).parent

    if not any(folder_path.iterdir()):
        folder_path.rmdir()
