# Generated by Django 3.2.2 on 2021-12-03 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_auto_20211202_0708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='desk',
            name='menus',
            field=models.ManyToManyField(to='market.Menu', verbose_name='menus'),
        ),
    ]