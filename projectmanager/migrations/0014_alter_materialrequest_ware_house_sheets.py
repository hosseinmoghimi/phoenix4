# Generated by Django 3.2.2 on 2021-12-09 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0013_alter_employee_is_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialrequest',
            name='ware_house_sheets',
            field=models.ManyToManyField(blank=True, related_name='ware_house_sheets', to='projectmanager.WareHouseSheet', verbose_name='برگه های انبار'),
        ),
    ]
