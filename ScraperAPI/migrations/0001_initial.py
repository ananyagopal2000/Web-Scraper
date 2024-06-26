# Generated by Django 5.0.6 on 2024-05-21 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='request_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_id', models.CharField(max_length=300, unique=True)),
                ('no_urls_requested', models.IntegerField(blank=True, null=True)),
                ('no_urls_suubmitted', models.IntegerField(blank=True, null=True)),
                ('status', models.TextField()),
            ],
        ),
    ]
