from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.test.utils import override_settings
from django.urls import reverse

from feedback.models import Feedback, FileUpload


__all__ = []


class FormTests(TestCase):
    def test_context_form_feedback_get(self):
        response = Client().get(reverse("feedback:feedback"))

        self.assertIn("form", response.context)

        form = response.context["form"]
        pers = response.context["pers"]
        text = form.fields["text"]
        mail = pers.fields["mail"]

        self.assertEqual(text.label, "Текст")
        self.assertEqual(mail.label, "Почта")
        self.assertEqual(text.help_text, "Введите желаемый текст")
        self.assertEqual(mail.help_text, "Укажите свой почтовый адрес")

    def test_context_form_feedback_post(self):
        content = {
            "name": "test",
            "text": "test_text",
            "mail": "example@example.com",
        }

        response = Client().post(
            reverse("feedback:feedback"),
            content,
            follow=True,
        )

        self.assertIn("form", response.context)

        messages = list(response.context["messages"])

        self.assertEqual(len(messages), 1)

        message = messages[0]
        self.assertEqual(message.tags, "success")
        self.assertEqual(message.message, "Форма успешно отправлена!")

    def test_feedback_form_errors(self):
        invalid_data = {
            "name": "",
            "text": "",
            "mail": "exampleexample.com",
        }

        response = Client().post(
            reverse("feedback:feedback"),
            data=invalid_data,
        )

        self.assertFalse(response.context["form"].is_valid())
        self.assertFalse(response.context["pers"].is_valid())
        self.assertFormError(response, "form", "text", "Обязательное поле.")
        self.assertFormError(
            response,
            "pers",
            "mail",
            "Введите правильный адрес электронной почты.",
        )

    def test_valid_data_db(self):
        number_of_feedback = Feedback.objects.count()

        valid_data = {
            "name": "test",
            "text": "test_text",
            "mail": "example@example.com",
        }

        Client().post(
            reverse("feedback:feedback"),
            data=valid_data,
        )

        self.assertEqual(number_of_feedback + 1, Feedback.objects.count())

    def test_invalid_data_db(self):
        number_of_feedback = Feedback.objects.count()

        invalid_data = {
            "name": "",
            "text": "",
            "mail": "exampleexample.com",
        }

        Client().post(
            reverse("feedback:feedback"),
            data=invalid_data,
        )

        self.assertEqual(number_of_feedback, Feedback.objects.count())

    @override_settings(MEDIA_ROOT=settings.BASE_DIR / "media_tests")
    def test_upload_files(self):
        number_of_uploads = FileUpload.objects.count()

        valid_data = {
            "name": "test",
            "text": "test_text",
            "mail": "example@example.com",
        }

        file1 = SimpleUploadedFile("file1.txt", b"file_content1")
        file2 = SimpleUploadedFile("file2.txt", b"file_content2")
        file3 = SimpleUploadedFile("file3.txt", b"file_content3")

        valid_data["file"] = [file1, file2, file3]

        Client().post(
            reverse("feedback:feedback"),
            data=valid_data,
            follow=True,
        )

        self.assertEqual(number_of_uploads + 3, FileUpload.objects.count())
