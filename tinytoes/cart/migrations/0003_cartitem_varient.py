# Generated by Django 4.2.4 on 2023-09-07 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0004_alter_productsize_product'),
        ('cart', '0002_payment_orders_orderproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='varient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminapp.productsize'),
        ),
    ]
