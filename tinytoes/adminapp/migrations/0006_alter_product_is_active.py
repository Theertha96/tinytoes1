# Generated by Django 4.2.4 on 2023-09-20 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0005_product_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]