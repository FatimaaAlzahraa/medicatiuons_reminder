# Generated by Django 4.2.16 on 2025-03-06 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("medication", "0005_medication_stopped_by_datetime"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="medication",
            name="stopped_by_datetime",
        ),
        migrations.AddField(
            model_name="medication",
            name="duration",
            field=models.IntegerField(default=0),
        ),
    ]
