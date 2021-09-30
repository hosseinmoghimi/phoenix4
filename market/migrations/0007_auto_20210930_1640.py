# Generated by Django 3.2.2 on 2021-09-30 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0006_financialreport_off'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='header_image_origin',
            field=models.ImageField(blank=True, null=True, upload_to='market/images/Brand/Header/', verbose_name='تصویر سربرگ'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='image_origin',
            field=models.ImageField(blank=True, null=True, upload_to='market/images/Brand/', verbose_name='تصویر'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='old_price',
            field=models.IntegerField(default=0, verbose_name='قیمت بدون تخفیف'),
        ),
        migrations.AlterField(
            model_name='supplier',
            name='logo_origin',
            field=models.ImageField(blank=True, null=True, upload_to='market/images/suppier/logo/', verbose_name='logo'),
        ),
    ]
