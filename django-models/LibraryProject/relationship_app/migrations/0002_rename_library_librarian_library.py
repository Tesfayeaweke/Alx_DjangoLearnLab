# Generated by Django 5.2.4 on 2025-07-20 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('relationship_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='librarian',
            old_name='Library',
            new_name='library',
        ),
    ]
