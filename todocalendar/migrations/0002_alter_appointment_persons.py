# Generated by Django 3.2.2 on 2021-11-08 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('todocalendar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='persons',
            field=models.ManyToManyField(blank=True, to='authentication.Profile', verbose_name='persons'),
        ),
    ]