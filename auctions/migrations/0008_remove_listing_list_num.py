# Generated by Django 5.1.2 on 2025-01-22 06:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_listing_list_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='list_num',
        ),
    ]
