# Generated by Django 3.2.2 on 2021-10-14 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0004_employeedocument'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='unit_name',
            field=models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته')], default='عدد', max_length=50, verbose_name='unit_name'),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('DEFAULT', 'DEFAULT'), ('تعریف اولیه در سیستم', 'تعریف اولیه در سیستم'), ('تحویل شده', 'تحویل شده'), ('در حال انجام', 'در حال انجام'), ('رد شده', 'رد شده'), ('پذیرفته شده', 'پذیرفته شده'), ('درخواست شده', 'درخواست شده'), ('در حال خرید', 'در حال خرید'), ('متعلق به کارفرما', 'متعلق به کارفرما'), ('موجود در انبار', 'موجود در انبار'), ('خارج شده از انبار', 'خارج شده از انبار'), ('وارد شده به انبار', 'وارد شده به انبار')], default='درخواست شده', max_length=50, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='request',
            name='unit_name',
            field=models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته')], default='عدد', max_length=50, verbose_name='واحد'),
        ),
        migrations.AlterField(
            model_name='warehousematerial',
            name='unit_name',
            field=models.CharField(blank=True, choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته')], max_length=50, null=True, verbose_name='unit_name'),
        ),
        migrations.AlterField(
            model_name='warehousesheetline',
            name='unit_name',
            field=models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته')], max_length=50, verbose_name='unit_name'),
        ),
    ]
