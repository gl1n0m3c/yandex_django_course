import profile
from django.shortcuts import get_object_or_404, render

from catalog.models import Item


__all__ = []


def base_item_list(request, items):
    template = "catalog/item_list.html"

    context = {"items": items}

    return render(request, template, context)


def item_list(request):
    items = Item.objects.get_item_list_page()
    return base_item_list(request, items)


def item_detail(request, pk):
    template = "catalog/item.html"

    item = get_object_or_404(
        Item.objects.get_item(),
        pk=pk,
    )

    context = {"item": item}

    return render(request, template, context)


def new(request):
    items = Item.objects.get_new()
    return base_item_list(request, items)


def friday(request):
    items = Item.objects.get_fridays()
    return base_item_list(request, items)


def unverified(request):
    items = Item.objects.get_unverified()
    return base_item_list(request, items)
