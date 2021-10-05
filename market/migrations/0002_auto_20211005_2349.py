# Generated by Django 3.2.2 on 2021-10-05 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس'),
        ),
        migrations.AddField(
            model_name='supplier',
            name='tel',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='تلفن'),
        ),
    ]
