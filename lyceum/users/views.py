from django.shortcuts import get_object_or_404, render, redirect
from django.conf import settings
from users.utils import send_activation_email
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone

from users.forms import SignUpForm
from users.models import Profile, UserProxy


def signup(request):
    form = SignUpForm(None or request.POST)

    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.is_active = settings.DEFAULT_USER_IS_ACTIVE
        user.save()

        send_activation_email(request, user)

        return redirect("users:login")

    template = "users/signup.html"
    context = {"form": form}
    return render(request, template, context)


def activate(request, name):
    user = get_object_or_404(User, username=name)

    if user.is_active:
        return HttpResponse("Аккаунт уже активирован")
    elif (timezone.now() - user.date_joined).seconds > 43200:
        return HttpResponse("Ссылка уже истекла")
    else:
        user.is_active = True
        user.save()

    return redirect("users:login")


def login(request):
    return HttpResponse("okey")


def user_list(request):
    users = UserProxy.objects.active()

    template = "users/user_list.html"
    context = {"users": users}

    return render(request, template, context)


@login_required
def user_detail(request, pk):
    user = get_object_or_404(
        UserProxy,
        pk=pk,
    )

    template = "users/profile.html"
    context = {"user": user}

    return render(request, template, context)
