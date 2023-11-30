from http import HTTPStatus

from django.http import HttpResponse
from django.shortcuts import render

from catalog.models import Item
from homepage.forms import EchoForm


__all__ = []


def home(request):
    template = "homepage/main.html"
    items = Item.objects.on_main()

    context = {"items": items}

    return render(request, template, context)


def coffee(request):
    return HttpResponse("Я чайник", status=HTTPStatus.IM_A_TEAPOT)


def echo(request):
    if request.method == "GET":
        template = "homepage/echo.html"

        form = EchoForm()

        context = {"form": form}

        return render(request, template, context)

    return HttpResponse("no POST!", status=HTTPStatus.METHOD_NOT_ALLOWED)


def echo_submit(request):
    form = EchoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        text = form.cleaned_data["text"]
        return HttpResponse(text, content_type="text/plain; charset=utf-8")

    return HttpResponse(
        "no no no bro)",
        status=HTTPStatus.METHOD_NOT_ALLOWED,
    )
