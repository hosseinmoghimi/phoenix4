# Generated by Django 3.2.2 on 2022-02-05 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hesabyar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehousesheet',
            name='ware_house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.warehouse', verbose_name='ware_house'),
        ),
    ]
