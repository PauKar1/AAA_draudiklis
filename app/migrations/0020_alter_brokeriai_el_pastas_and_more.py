# Generated by Django 4.2.13 on 2024-06-02 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0019_alter_profile_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="brokeriai",
            name="el_pastas",
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name="brokeriai",
            name="tel_numeris",
            field=models.IntegerField(null=True),
        ),
    ]
