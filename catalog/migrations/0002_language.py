# Generated by Django 5.1.5 on 2025-02-06 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Language",
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
                (
                    "name",
                    models.CharField(
                        help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)",
                        max_length=200,
                        unique=True,
                    ),
                ),
                (
                    "book_instance",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="catalog.bookinstance",
                    ),
                ),
            ],
        ),
    ]
