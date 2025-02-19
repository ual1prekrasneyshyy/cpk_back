# Generated by Django 5.1.6 on 2025-02-17 08:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_cartitem_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='items', to='shop.cart'),
        ),
    ]
