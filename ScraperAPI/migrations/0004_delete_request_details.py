# Generated by Django 5.0.6 on 2024-05-22 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ScraperAPI', '0003_delete_url_details'),
    ]

    operations = [
        migrations.DeleteModel(
            name='request_details',
        ),
    ]
