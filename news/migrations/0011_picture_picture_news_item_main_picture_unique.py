# Generated by Django 5.0.7 on 2024-08-12 08:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("news", "0010_alter_newsitem_text"),
    ]

    operations = [
        migrations.CreateModel(
            name="Picture",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "picture",
                    models.ImageField(
                        upload_to="news/pictures/", verbose_name="picture"
                    ),
                ),
                (
                    "main_picture",
                    models.BooleanField(
                        default=False,
                        help_text="The main pictrure is the picture shown on the cover of the news item.",
                        verbose_name="main picture",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "news_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pictures",
                        to="news.newsitem",
                        verbose_name="news item",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="picture",
            constraint=models.UniqueConstraint(
                condition=models.Q(("main_picture", True)),
                fields=("news_item", "main_picture"),
                name="news_item_main_picture_unique",
                violation_error_message="Only one picture can be the main picture for a news item",
            ),
        ),
    ]