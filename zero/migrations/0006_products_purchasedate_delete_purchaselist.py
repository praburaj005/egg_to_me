# Generated by Django 5.1.7 on 2025-03-27 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zero', '0005_alter_invoice_total_alter_invoicelist_invoiceid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='purchasedate',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.DeleteModel(
            name='PurchaseList',
        ),
    ]
