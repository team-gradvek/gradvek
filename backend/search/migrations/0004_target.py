# Generated by Django 4.1.7 on 2023-04-04 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_rename_descriptors_descriptor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=60)),
            ],
        ),
    ]