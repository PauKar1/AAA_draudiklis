# Generated by Django 4.2.13 on 2024-05-30 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0006_alter_polisai_iskaita"),
    ]

    operations = [
        migrations.CreateModel(
            name="Country",
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
                ("name", models.CharField(max_length=100)),
                ("risk_level", models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name="klientai",
            name="user",
        ),
    ]
