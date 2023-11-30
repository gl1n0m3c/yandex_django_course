from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from feedback.forms import FeedbackForm, FileFeedbackForm, PersonalDataForm
from feedback.models import FileUpload


__all__ = []


def feedback(request):
    template = "feedback/feedback.html"

    form = FeedbackForm(request.POST or None)
    pers = PersonalDataForm(request.POST or None)
    fileform = FileFeedbackForm(request.POST or None, request.FILES or None)

    if (
        request.method == "POST"
        and form.is_valid()
        and fileform.is_valid()
        and pers.is_valid()
    ):
        send_mail(
            "Feedback",
            form.cleaned_data["text"],
            settings.MAIL,
            [
                pers.cleaned_data["mail"],
            ],
            fail_silently=False,
        )

        feedback_instance = form.save()

        pers_instance = pers.save(commit=False)

        pers_instance.feedback = feedback_instance
        pers_instance.save()

        files = fileform.cleaned_data["file"]
        for file in files:
            FileUpload.objects.create(
                feedback=feedback_instance,
                file=file,
            )

        messages.success(request, "Форма успешно отправлена!")

        return redirect("feedback:feedback")

    context = {
        "pers": pers,
        "form": form,
        "fileform": fileform,
    }

    return render(request, template, context)
