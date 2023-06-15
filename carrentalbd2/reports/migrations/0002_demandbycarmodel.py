# Generated by Django 4.2 on 2023-06-14 21:39

from django.db import migrations, models
import django_matplotlib.fields


class Migration(migrations.Migration):

    dependencies = [("reports", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="DemandByCarModel",
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