# Generated by Django 3.2.2 on 2021-11-01 20:41

import accounting.models
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('market', '0002_auto_20211005_2349'),
        ('authentication', '0001_initial'),
        ('core', '0003_alter_link_new_tab'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountingPage',
            fields=[
                ('basicpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.basicpage')),
            ],
            bases=('core.basicpage',),
        ),
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_name', models.CharField(blank=True, max_length=50, verbose_name='app_name')),
                ('class_name', models.CharField(blank=True, max_length=50, verbose_name='class_name')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('price', models.IntegerField(default=0, verbose_name='price')),
                ('year', models.IntegerField(verbose_name='سال ساخت')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='accounting/images/Property', verbose_name='image')),
                ('owner', models.CharField(blank=True, max_length=50, null=True, verbose_name='مالک')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date_updated')),
                ('description', tinymce.models.HTMLField(blank=True, max_length=5000, null=True, verbose_name='توضیحات')),
            ],
            options={
                'verbose_name': 'Asset',
                'verbose_name_plural': 'Assets',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('accountingpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.accountingpage')),
                ('amount', models.IntegerField(default=0, verbose_name='amount')),
                ('date_paid', models.DateTimeField(verbose_name='date_paid')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
            bases=('accounting.accountingpage',),
        ),
        migrations.CreateModel(
            name='FinancialAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'FinancialAccount',
                'verbose_name_plural': 'FinancialAccounts',
            },
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('bank', models.CharField(choices=[('بانک ملی', 'بانک ملی'), ('بانک ملت', 'بانک ملت'), ('بانک سپه', 'بانک سپه'), ('بانک رفاه', 'بانک رفاه'), ('بانک مسکن', 'بانک مسکن'), ('بانک توسعه تعاون', 'بانک توسعه تعاون')], max_length=50, verbose_name='bank')),
                ('branch', models.CharField(max_length=50, verbose_name='شعبه')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.financialaccount', verbose_name='owner')),
            ],
            options={
                'verbose_name': 'BankAccount',
                'verbose_name_plural': 'BankAccounts',
            },
        ),
        migrations.CreateModel(
            name='MoneyTransaction',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.transaction')),
                ('payment_method', models.CharField(choices=[('وجه نقد', 'وجه نقد'), ('کارت به کارت', 'کارت به کارت'), ('واریزی بانک', 'واریزی بانک'), ('چک', 'چک')], default='کارت به کارت', max_length=50, verbose_name='payment_method')),
            ],
            options={
                'verbose_name': 'MoneyTransaction',
                'verbose_name_plural': 'MoneyTransactions',
            },
            bases=('accounting.transaction', accounting.models.TransactionMixin),
        ),
        migrations.AddField(
            model_name='transaction',
            name='pay_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pay_from_set', to='accounting.financialaccount', verbose_name='pay_from'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='pay_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pay_to_set', to='accounting.financialaccount', verbose_name='pay_to'),
        ),
        migrations.CreateModel(
            name='MarketOrderTransaction',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.transaction')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.order', verbose_name='order')),
            ],
            options={
                'verbose_name': 'MarketOrderTransaction',
                'verbose_name_plural': 'MarketOrderTransactions',
            },
            bases=('accounting.transaction', accounting.models.TransactionMixin),
        ),
        migrations.CreateModel(
            name='AssetTransaction',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.transaction')),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounting.asset', verbose_name='asset')),
            ],
            options={
                'verbose_name': 'AssetTransaction',
                'verbose_name_plural': 'AssetTransactions',
            },
            bases=('accounting.transaction', accounting.models.TransactionMixin),
        ),
    ]
