# Generated by Django 3.2.2 on 2021-06-25 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_carousel_height'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carousel',
            name='height',
            field=models.IntegerField(default=350, verbose_name='height'),
        ),
    ]
