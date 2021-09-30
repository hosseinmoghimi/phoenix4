# Generated by Django 3.2.2 on 2021-09-30 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0002_request_request_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicerequest',
            name='service',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='projectmanager.service', verbose_name='service'),
            preserve_default=False,
        ),
    ]
