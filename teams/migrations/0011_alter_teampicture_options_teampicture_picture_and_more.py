# Generated by Django 5.0.7 on 2024-08-15 21:45

import django.db.models.deletion
import teams.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("teams", "0010_auto_20240815_2335"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="teampicture",
            options={
                "verbose_name": "team picture",
                "verbose_name_plural": "team pictures",
            },
        ),
        migrations.AddField(
            model_name="teampicture",
            name="picture",
            field=models.ImageField(
                default="test",
                upload_to=teams.models.team_season_path,
                verbose_name="picture",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="teampicture",
            name="season",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to="teams.season",
                verbose_name="season",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="teampicture",
            name="team",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="teams.team",
                verbose_name="team",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="team",
            name="number_pool",
            field=models.ForeignKey(
                default="default",
                on_delete=django.db.models.deletion.PROTECT,
                to="teams.numberpool",
                to_field="name",
                verbose_name="number pool",
            ),
        ),
    ]
