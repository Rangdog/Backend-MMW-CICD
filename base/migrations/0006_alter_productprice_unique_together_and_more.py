# Generated by Django 5.0.6 on 2024-06-05 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_pricelist_options_remove_product_in_stock_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productprice',
            unique_together={('pricelist', 'product')},
        ),
        migrations.AlterModelTable(
            name='exportdetail',
            table='ExportDetail',
        ),
        migrations.AlterModelTable(
            name='importdetail',
            table='ImportDetail',
        ),
        migrations.AlterModelTable(
            name='orderdetail',
            table='OrderDetail',
        ),
        migrations.AlterModelTable(
            name='productprice',
            table='ProductPrice',
        ),
    ]