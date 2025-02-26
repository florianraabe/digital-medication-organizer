# Generated by Django 5.1.4 on 2025-01-21 13:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("MedApp", "0007_alter_medication_enddate"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="medication",
            options={
                "ordering": ["-creation_date"],
                "verbose_name": "Medication",
                "verbose_name_plural": "Medication",
            },
        ),
        migrations.AddField(
            model_name="medication",
            name="creation_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
