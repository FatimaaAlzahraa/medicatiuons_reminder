# Generated by Django 4.2.16 on 2025-03-15 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("medication", "0007_remove_medication_duration_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="medication",
            name="is_chronic_or_acute",
        ),
    ]
