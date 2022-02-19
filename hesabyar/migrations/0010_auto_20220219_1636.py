# Generated by Django 3.2.2 on 2022-02-19 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20220217_1833'),
        ('hesabyar', '0009_auto_20220217_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='links',
            field=models.ManyToManyField(blank=True, to='core.Link', verbose_name='links'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='payment_method',
            field=models.CharField(choices=[('پیش نویس', 'پیش نویس'), ('پرداخت نشده', 'پرداخت نشده'), ('همراه بانک', 'همراه بانک'), ('نقدی', 'نقدی'), ('چک', 'چک'), ('کارتخوان', 'کارتخوان'), ('کارت به کارت', 'کارت به کارت')], default='پیش نویس', max_length=50, verbose_name='نوع پرداخت'),
        ),
    ]
