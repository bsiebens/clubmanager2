# Generated by Django 5.1.1 on 2024-10-20 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0020_rename_children_member_family_members"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Family",
        ),
    ]