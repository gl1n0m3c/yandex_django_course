# Generated by Django 4.2.5 on 2023-10-31 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0006_alter_category_options_alter_item_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="normalization",
            field=models.CharField(
                editable=False,
                max_length=150,
                null=True,
                unique=True,
                verbose_name="нормализированное имя",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="category",
            field=models.ForeignKey(
                help_text="Выберите категорию",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                related_query_name="category",
                to="catalog.category",
                verbose_name="категория",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="main_image",
            field=models.OneToOneField(
                blank=True,
                help_text="Выберите главное изображение товара",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
                related_query_name="main_image",
                to="catalog.mainimagemodel",
                verbose_name="главное изображение",
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="tags",
            field=models.ManyToManyField(
                help_text="Выберите теги, описывающие данный товар.",
                related_name="items",
                related_query_name="tags",
                to="catalog.tag",
            ),
        ),
        migrations.AlterField(
            model_name="manyimagemodel",
            name="image",
            field=models.ImageField(
                upload_to="extra_images", verbose_name="изображение"
            ),
        ),
        migrations.AlterField(
            model_name="manyimagemodel",
            name="item",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                related_query_name="items",
                to="catalog.item",
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="normalization",
            field=models.CharField(
                editable=False,
                max_length=150,
                null=True,
                unique=True,
                verbose_name="нормализированное имя",
            ),
        ),
    ]
