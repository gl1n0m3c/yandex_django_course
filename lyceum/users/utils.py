from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site


def send_activation_email(request, user):
    current_site = get_current_site(request)
    activation_link = f"{current_site.domain}/users/activate/{user.username}"

    subject = "Активация аккаунта"
    message = f"Спасибо за регистрацию. Для активации аккаунта перейдите по ссылке:\n\n{activation_link}"

    send_mail(
        subject,
        message,
        settings.MAIL,
        [user.email],
        fail_silently=False,
    )
