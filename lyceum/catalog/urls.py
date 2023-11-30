from django.urls import path, register_converter

from catalog import converters, views


app_name = "catalog"

register_converter(converters.DigitConverter, "digit_conv")

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("<int:pk>/", views.item_detail, name="item_detail"),
    path("new/", views.new, name="new"),
    path("friday/", views.friday, name="friday"),
    path("unverified/", views.unverified, name="unverified"),
]
