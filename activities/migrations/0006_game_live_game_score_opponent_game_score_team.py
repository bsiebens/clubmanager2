# Generated by Django 5.1.1 on 2024-09-07 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("activities", "0005_competition_game_competition"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="live",
            field=models.BooleanField(default=False, verbose_name="live"),
        ),
        migrations.AddField(
            model_name="game",
            name="score_opponent",
            field=models.IntegerField(default=0, verbose_name="score opponent"),
        ),
        migrations.AddField(
            model_name="game",
            name="score_team",
            field=models.IntegerField(default=0, verbose_name="score team"),
        ),
    ]