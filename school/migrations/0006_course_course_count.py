# Generated by Django 3.2.2 on 2021-12-24 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0005_auto_20211207_0253'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_count',
            field=models.IntegerField(default=1, verbose_name='تعداد واحد'),
            preserve_default=False,
        ),
    ]