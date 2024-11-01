#  Copyright (c) 2024. https://github.com/bsiebens/ClubManager

# Generated by Django 5.1.1 on 2024-10-29 17:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("finance", "0012_remove_material_role_remove_material_team_and_more"),
        ("teams", "0016_alter_team_number_pool"),
    ]

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "description",
                    models.CharField(
                        blank=True,
                        max_length=250,
                        null=True,
                        verbose_name="description",
                    ),
                ),
                (
                    "unit_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=7, verbose_name="price"
                    ),
                ),
                (
                    "unit_price_type",
                    models.IntegerField(
                        choices=[(0, "amount"), (1, "percentage")],
                        default=0,
                        verbose_name="price type",
                    ),
                ),
                (
                    "member_required",
                    models.BooleanField(
                        default=False,
                        help_text="Select if this item requires a member to be associated with it when creating an order",
                        verbose_name="member required",
                    ),
                ),
                (
                    "role",
                    models.ForeignKey(
                        blank=True,
                        help_text="Optional, select a role for which an item should be created",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="teams.teamrole",
                        verbose_name="team role",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        blank=True,
                        help_text="Optional, select a team for which an item should be created",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="teams.team",
                        verbose_name="team",
                    ),
                ),
            ],
            options={
                "verbose_name": "item",
                "verbose_name_plural": "items",
                "ordering": ["description"],
            },
        ),
    ]