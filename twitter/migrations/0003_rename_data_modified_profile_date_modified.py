# Generated by Django 4.1.3 on 2024-01-30 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0002_profile_data_modified'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='data_modified',
            new_name='date_modified',
        ),
    ]
