# Generated by Django 4.1.7 on 2023-03-19 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_rename_bid_listings_start_price_alter_comment_item_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='listing',
        ),
        migrations.RemoveField(
            model_name='listings',
            name='start_price',
        ),
        migrations.AddField(
            model_name='listings',
            name='bid_price',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bidPrice', to='auctions.bid'),
        ),
    ]
