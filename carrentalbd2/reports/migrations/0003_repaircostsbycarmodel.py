# Generated by Django 4.2 on 2023-06-14 22:14

from django.db import migrations, models
import django_matplotlib.fields


class Migration(migrations.Migration):

    dependencies = [("reports", "0002_demandbycarmodel")]

    operations = [
        migrations.CreateModel(
            name="RepairCostsByCarModel",
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
                ("figure", django_matplotlib.fields.MatplotlibFigureField()),
            ],
        )
    ]
