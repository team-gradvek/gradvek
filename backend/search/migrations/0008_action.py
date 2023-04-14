# Generated by Django 4.2 on 2023-04-12 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("search", "0007_rename_descriptor_name_descriptor_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Action",
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
                ("action", models.CharField(max_length=30)),
                ("count", models.IntegerField()),
            ],
        ),
    ]