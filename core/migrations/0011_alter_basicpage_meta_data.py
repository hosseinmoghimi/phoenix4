# Generated by Django 3.2.2 on 2021-12-29 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_document_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicpage',
            name='meta_data',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='کلیدواژه ها یا متا دیتا'),
        ),
    ]