# Generated by Django 4.2.4 on 2023-09-23 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0009_alter_product_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='offer_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
