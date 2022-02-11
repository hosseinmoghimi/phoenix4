# Generated by Django 3.2.2 on 2022-02-11 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0016_sampleform'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='unit_name',
            field=models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته'), ('کیسه', 'کیسه'), ('شات', 'شات'), ('فنجان', 'فنجان'), ('جفت', 'جفت')], default='عدد', max_length=50, verbose_name='unit_name'),
        ),
        migrations.AlterField(
            model_name='request',
            name='unit_name',
            field=models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته'), ('کیسه', 'کیسه'), ('شات', 'شات'), ('فنجان', 'فنجان'), ('جفت', 'جفت')], default='عدد', max_length=50, verbose_name='واحد'),
        ),
        migrations.AlterField(
            model_name='warehousematerial',
            name='unit_name',
            field=models.CharField(blank=True, choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته'), ('کیسه', 'کیسه'), ('شات', 'شات'), ('فنجان', 'فنجان'), ('جفت', 'جفت')], max_length=50, null=True, verbose_name='unit_name'),
        ),
        migrations.AlterField(
            model_name='warehousesheetline',
            name='unit_name',
            field=models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته'), ('کیسه', 'کیسه'), ('شات', 'شات'), ('فنجان', 'فنجان'), ('جفت', 'جفت')], max_length=50, verbose_name='unit_name'),
        ),
    ]
