# Generated by Django 3.2.3 on 2021-05-29 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("plans", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="plan",
            old_name="thumbnail_sizes",
            new_name="available_thumbnail_sizes",
        ),
    ]
