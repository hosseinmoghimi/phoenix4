# Generated by Django 3.2.2 on 2021-10-08 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0004_auto_20211009_0044'),
    ]

    operations = [
        migrations.RenameField(
            model_name='warehousematerial',
            old_name='quantity_origin',
            new_name='sum_quantity_origin',
        ),
    ]
