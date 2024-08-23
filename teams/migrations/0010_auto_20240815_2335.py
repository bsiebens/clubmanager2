# Generated by Django 5.0.7 on 2024-08-15 21:35

from django.db import migrations


def create_default_pool(apps, schema_editor):
    NumberPool = apps.get_model("teams", "NumberPool")

    try:
        NumberPool.objects.create(name="default", enforce_unique=False)

    except:
        pass


def remove_number_pool(apps, schema_editor):
    NumberPool = apps.get_model("teams", "NumberPool")

    if NumberPool.objects.get(name="default").exists():
        NumberPool.objects.get(name="default").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0009_teammembership_team_season_number_unique"),
    ]

    operations = [migrations.RunPython(create_default_pool, remove_number_pool)]