# Generated by Django 5.1.1 on 2024-10-26 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("activities", "0015_game_game_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="gametype",
            name="opponent_count",
            field=models.IntegerField(
                default=1,
                help_text="Number of opponents for this game type",
                verbose_name="opponent count",
            ),
        ),
    ]
