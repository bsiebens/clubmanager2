# Generated by Django 5.1.1 on 2024-09-08 13:24

from django.db import migrations


def create_competiton_group(apps, schema_editor):
    Competition = apps.get_model("activities", "Competition")

    try:
        Competition.objects.create(name="CEHL", module="activities.competition.hockey")

    except:
        pass


def remove_competiton_group(apps, schema_editor):
    Competition = apps.get_model("activities", "Competition")

    try:
        Competition.objects.get(name="CEHL", module="activities.competition.hockey").delete()

    except:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ("activities", "0008_auto_20240907_2231"),
    ]

    operations = [migrations.RunPython(create_competiton_group, remove_competiton_group)]