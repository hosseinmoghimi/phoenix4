# Generated by Django 3.2.2 on 2022-02-08 15:10

from django.db import migrations, models
import django.db.models.deletion
import hesabyar.models


class Migration(migrations.Migration):

    dependencies = [
        ('hesabyar', '0006_invoice_payment_method'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cheque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('cheque_date', models.DateField(verbose_name='تاریخ چک')),
                ('description', models.CharField(blank=True, max_length=50, null=True, verbose_name='توضیحات')),
                ('amount', models.IntegerField(verbose_name='مبلغ')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cheque_owned', to='hesabyar.profilefinancialaccount', verbose_name='owner')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cheque_received', to='hesabyar.profilefinancialaccount', verbose_name='receiver')),
            ],
            options={
                'verbose_name': 'چک',
                'verbose_name_plural': 'چک ها',
            },
            bases=(models.Model, hesabyar.models.LinkHelper),
        ),
    ]
