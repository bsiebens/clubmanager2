# Generated by Django 5.1.1 on 2024-10-27 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("activities", "0018_delete_competition"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gametype",
            name="opponent_count",
            field=models.IntegerField(
                default=1,
                help_text="Number of opponents for this game type, does not have any influence on the working of clubmanager but is passed along in the API.",
                verbose_name="opponent count",
            ),
        ),
    ]