# Generated by Django 3.2.2 on 2021-08-12 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='image_origin',
            field=models.ImageField(blank=True, null=True, upload_to='messenger/images/channel/', verbose_name='image'),
        ),
    ]
