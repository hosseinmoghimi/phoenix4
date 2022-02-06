# Generated by Django 3.2.2 on 2022-02-06 18:48

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('hesabyar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('پیش فاکتور', 'پیش فاکتور'), ('در جریان', 'در جریان'), ('تحویل شده', 'تحویل شده')], default='پیش فاکتور', max_length=50, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.profilefinancialaccount', verbose_name='مشتری'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='description',
            field=tinymce.models.HTMLField(blank=True, max_length=50000, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.store', verbose_name='فروشنده'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='tax_percent',
            field=models.IntegerField(default=9, verbose_name='درصد مالیات'),
        ),
    ]