# Generated by Django 5.2.1 on 2025-06-09 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dms', '0002_alter_directmessage_receiver_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]
