# Generated by Django 5.0.7 on 2024-09-05 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0015_remove_family_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="member",
            name="license",
            field=models.CharField(
                default="TBD", max_length=250, verbose_name="license"
            ),
            preserve_default=False,
        ),
    ]