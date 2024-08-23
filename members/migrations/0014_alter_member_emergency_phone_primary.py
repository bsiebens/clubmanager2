# Generated by Django 5.0.7 on 2024-08-06 20:29

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0013_alter_member_birthday"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="emergency_phone_primary",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True,
                max_length=128,
                null=True,
                region=None,
                verbose_name="first emergency phone",
            ),
        ),
    ]