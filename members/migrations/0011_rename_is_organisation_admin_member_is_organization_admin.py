# Generated by Django 5.0.7 on 2024-08-03 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0010_member_is_organisation_admin"),
    ]

    operations = [
        migrations.RenameField(
            model_name="member",
            old_name="is_organisation_admin",
            new_name="is_organization_admin",
        ),
    ]