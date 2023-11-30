from django.contrib import admin

from catalog.models import Category, Item, MainImageModel, ManyImageModel, Tag


__all__ = []


class ImagesInline(admin.StackedInline):
    model = ManyImageModel


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = [
        Item.name.field.name,
        Item.is_published.field.name,
        Item.is_on_main.field.name,
        Item.main_image.field.name,
    ]
    list_editable = [Item.is_published.field.name, Item.is_on_main.field.name]
    list_display_links = [Item.name.field.name]
    filter_horizontal = [Item.tags.field.name]
    inlines = [ImagesInline]
    readonly_fields = [Item.created.field.name, Item.updated.field.name]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = [
        Tag.name.field.name,
        Tag.is_published.field.name,
        Tag.slug.field.name,
    ]
    list_editable = [Tag.is_published.field.name]
    list_display_links = [Tag.name.field.name]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        Category.name.field.name,
        Category.is_published.field.name,
        Category.slug.field.name,
    ]
    list_editable = [Category.is_published.field.name]
    list_display_links = [Category.name.field.name]


@admin.register(MainImageModel)
class MainImageAdmin(admin.ModelAdmin):
    list_display = [
        MainImageModel.name.field.name,
        MainImageModel.display_image,
    ]
    list_display_links = [MainImageModel.name.field.name]


@admin.register(ManyImageModel)
class ManyImageAdmin(admin.ModelAdmin):
    list_display = [
        ManyImageModel.name.field.name,
        ManyImageModel.display_image,
    ]
    list_display_links = [ManyImageModel.name.field.name]
