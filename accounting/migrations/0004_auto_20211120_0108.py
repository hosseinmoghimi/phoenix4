# Generated by Django 3.2.2 on 2021-11-19 21:38

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0003_auto_20211112_0059'),
    ]

    operations = [
        migrations.AddField(
            model_name='bankaccount',
            name='description',
            field=tinymce.models.HTMLField(blank=True, max_length=5000, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='bankaccount',
            name='bank',
            field=models.CharField(choices=[('بانک ملی', 'بانک ملی'), ('بانک ملت', 'بانک ملت'), ('بانک سپه', 'بانک سپه'), ('بانک رفاه', 'بانک رفاه'), ('بانک صادرات', 'بانک صادرات'), ('بانک مسکن', 'بانک مسکن'), ('بانک توسعه تعاون', 'بانک توسعه تعاون')], max_length=50, verbose_name='بانک'),
        ),
    ]
