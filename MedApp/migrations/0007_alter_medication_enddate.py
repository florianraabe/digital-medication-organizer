# Generated by Django 5.1.3 on 2024-12-04 14:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("MedApp", "0006_medication_enddate"),
    ]

    operations = [
        migrations.AlterField(
            model_name="medication",
            name="enddate",
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name="Date until the medication needs to be taken",
            ),
        ),
    ]
