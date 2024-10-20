# Generated by Django 4.2.2 on 2024-10-20 18:16

from django.db import migrations, models
import expenses.models


class Migration(migrations.Migration):

    dependencies = [
        ("expenses", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="mobile",
            field=models.CharField(
                max_length=10, validators=[expenses.models.validate_mobile_number]
            ),
        ),
    ]