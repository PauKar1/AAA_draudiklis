# Generated by Django 4.2.13 on 2024-06-04 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0026_remove_polisai_apsauga_polisai_cover1_polisai_cover2_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="polisai",
            name="draudimo_suma",
        ),
    ]