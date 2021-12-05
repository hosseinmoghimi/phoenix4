# Generated by Django 3.2.2 on 2021-12-05 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0003_alter_location_title'),
        ('projectmanager', '0011_employee_is_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='locations',
            field=models.ManyToManyField(blank=True, to='map.Location', verbose_name='locations'),
        ),
    ]
