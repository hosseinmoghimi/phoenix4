# Generated by Django 3.2.2 on 2021-11-09 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='col',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='col'),
        ),
        migrations.AddField(
            model_name='book',
            name='row',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='row'),
        ),
        migrations.AddField(
            model_name='book',
            name='shelf',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='shelf'),
        ),
    ]