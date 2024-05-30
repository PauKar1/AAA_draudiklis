# Generated by Django 4.2.13 on 2024-05-30 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0008_country_continent_country_latitude_country_longitude"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="country",
            name="continent",
        ),
        migrations.AlterField(
            model_name="country",
            name="latitude",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="country",
            name="longitude",
            field=models.FloatField(),
        ),
    ]