# Generated by Django 5.0.7 on 2024-08-26 06:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0014_alter_member_emergency_phone_primary"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="family",
            name="name",
        ),
    ]
