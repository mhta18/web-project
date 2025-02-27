# Generated by Django 5.1.2 on 2025-01-21 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='is_active',
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.CharField(default='other', max_length=100),
        ),
        migrations.AlterField(
            model_name='listing',
            name='created_at',
            field=models.DateTimeField(default='2025/01/21'),
        ),
    ]
