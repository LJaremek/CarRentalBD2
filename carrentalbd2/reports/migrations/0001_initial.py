# Generated by Django 4.2 on 2023-06-14 17:20

from django.db import migrations, models
import django_matplotlib.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BrandOrigin",
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
        ),
        migrations.CreateModel(
            name="CarByBrand",
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
        ),
        migrations.CreateModel(
            name="RepairRealization",
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
        ),
    ]
