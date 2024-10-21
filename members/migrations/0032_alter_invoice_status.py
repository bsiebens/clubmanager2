# Generated by Django 5.1.1 on 2024-10-21 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("members", "0031_alter_lineitem_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="invoice",
            name="status",
            field=models.IntegerField(
                choices=[(0, "New"), (1, "Submitted"), (2, "Invoiced"), (3, "Payed")],
                default=0,
                verbose_name="status",
            ),
        ),
    ]
