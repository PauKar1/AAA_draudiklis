# Generated by Django 4.2.13 on 2024-05-31 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0015_alter_klientai_adresas_alter_klientai_el_pastas_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="klientai",
            name="adresas",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="klientai",
            name="el_pastas",
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name="klientai",
            name="gimimo_data",
            field=models.DateField(),
        ),
    ]
