# Generated by Django 4.1.7 on 2023-03-19 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_remove_bid_listing_remove_listings_start_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listings',
            name='bid_price',
        ),
        migrations.AddField(
            model_name='listings',
            name='price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.bid'),
        ),
        migrations.AlterField(
            model_name='bid',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]
