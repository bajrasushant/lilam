# Generated by Django 4.1.7 on 2023-03-19 10:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_remove_listings_bid_price_listings_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listings',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]