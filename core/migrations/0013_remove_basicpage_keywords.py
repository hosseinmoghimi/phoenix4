# Generated by Django 3.2.2 on 2022-01-06 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_basicpage_meta_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basicpage',
            name='keywords',
        ),
    ]
