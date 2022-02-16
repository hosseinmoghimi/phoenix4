# Generated by Django 3.2.2 on 2022-02-16 20:43

from django.db import migrations, models
import django.db.models.deletion
import hesabyar.models


class Migration(migrations.Migration):

    dependencies = [
        ('hesabyar', '0005_auto_20220215_0315'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sell_benefit', models.IntegerField(default=0, verbose_name='سود حاصل از فروش')),
                ('sell_loss', models.IntegerField(default=0, verbose_name='زیان حاصل از فروش')),
                ('cost', models.IntegerField(default=0, verbose_name='هزینه')),
                ('tax', models.IntegerField(default=0, verbose_name='مالیات')),
                ('sell_service', models.IntegerField(default=0, verbose_name='فروش خدمات')),
                ('buy_service', models.IntegerField(default=0, verbose_name='خرید خدمات')),
                ('ship_fee', models.IntegerField(default=0, verbose_name='هزینه حمل')),
                ('financial_document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.financialdocument', verbose_name='FinancialDocument')),
            ],
            options={
                'verbose_name': 'FinancialBalance',
                'verbose_name_plural': 'FinancialBalances',
            },
            bases=(models.Model, hesabyar.models.LinkHelper),
        ),
    ]