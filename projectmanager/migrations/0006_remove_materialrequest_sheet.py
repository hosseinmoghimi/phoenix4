# Generated by Django 3.2.2 on 2021-10-06 20:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0005_auto_20211007_0002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materialrequest',
            name='sheet',
        ),
    ]
