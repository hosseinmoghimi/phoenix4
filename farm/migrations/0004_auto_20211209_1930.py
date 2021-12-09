# Generated by Django 3.2.2 on 2021-12-09 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farm', '0003_auto_20211020_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='unit_name',
            field=models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته'), ('کیسه', 'کیسه'), ('شات', 'شات'), ('فنجان', 'فنجان')], default='کیلوگرم', max_length=50, verbose_name='unit_name'),
        ),
        migrations.AlterField(
            model_name='saloonfood',
            name='unit_name',
            field=models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته'), ('کیسه', 'کیسه'), ('شات', 'شات'), ('فنجان', 'فنجان')], max_length=50, verbose_name='unit_name'),
        ),
    ]
