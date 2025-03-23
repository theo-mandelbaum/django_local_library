# Generated by Django 5.1.6 on 2025-03-04 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_rename_borrowed_bookinstance_borrower"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="author",
            options={
                "ordering": ["last_name", "first_name"],
                "permissions": (("can_mark_returned", "Set book as returned"),),
            },
        ),
    ]
