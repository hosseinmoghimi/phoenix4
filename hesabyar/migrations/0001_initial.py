# Generated by Django 3.2.2 on 2022-02-11 21:20

from django.db import migrations, models
import django.db.models.deletion
import hesabyar.models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0014_navlink_parent'),
        ('authentication', '0004_profile_header_origin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='بانک')),
                ('branch', models.CharField(blank=True, max_length=50, null=True, verbose_name='شعبه')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='آدرس')),
                ('tel', models.CharField(blank=True, max_length=50, null=True, verbose_name='تلفن')),
            ],
            options={
                'verbose_name': 'Bank',
                'verbose_name_plural': 'Banks',
            },
        ),
        migrations.CreateModel(
            name='FinancialAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, verbose_name='title')),
                ('class_name', models.CharField(blank=True, max_length=50, verbose_name='class_name')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hesabyar_accounts', to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'FinancialAccount',
                'verbose_name_plural': 'FinancialAccounts',
            },
        ),
        migrations.CreateModel(
            name='FinancialDocumentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='دسته بندی')),
                ('color', models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('rose', 'rose'), ('dark', 'dark')], default='primary', max_length=50, verbose_name='color')),
            ],
            options={
                'verbose_name': 'FinancialDocumentCategory',
                'verbose_name_plural': 'FinancialDocumentCategories',
            },
        ),
        migrations.CreateModel(
            name='FinancialYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('year', models.IntegerField(verbose_name='year')),
                ('start_date', models.DateTimeField(verbose_name='start_date')),
                ('end_date', models.DateTimeField(verbose_name='end_date')),
            ],
            options={
                'verbose_name': 'FinancialYear',
                'verbose_name_plural': 'FinancialYears',
            },
        ),
        migrations.CreateModel(
            name='HesabYarPage',
            fields=[
                ('basicpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.basicpage')),
            ],
            bases=('core.basicpage',),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('color', models.CharField(choices=[('success', 'success'), ('danger', 'danger'), ('warning', 'warning'), ('primary', 'primary'), ('secondary', 'secondary'), ('info', 'info'), ('light', 'light'), ('rose', 'rose'), ('dark', 'dark')], default='primary', max_length=50, verbose_name='color')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('status', models.CharField(choices=[('پیش نویس', 'پیش نویس'), ('در جریان', 'در جریان'), ('تحویل شده', 'تحویل شده'), ('تایید شده', 'تایید شده')], default='پیش نویس', max_length=50, verbose_name='وضعیت')),
                ('amount', models.IntegerField(default=0, verbose_name='مبلغ')),
                ('transaction_datetime', models.DateTimeField(verbose_name='transaction_datetime')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('payment_method', models.CharField(choices=[('نقدی', 'نقدی'), ('کارتخوان', 'کارتخوان'), ('کارت به کارت', 'کارت به کارت')], default='کارت به کارت', max_length=50, verbose_name='نوع پرداخت')),
                ('description', tinymce.models.HTMLField(blank=True, max_length=50000, null=True, verbose_name='توضیحات')),
                ('class_name', models.CharField(blank=True, max_length=50, verbose_name='class_name')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='ثبت شده توسط')),
                ('pay_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paid_set', to='hesabyar.financialaccount', verbose_name='بستانکار')),
                ('pay_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_set', to='hesabyar.financialaccount', verbose_name='بدهکار')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
            bases=(models.Model, hesabyar.models.LinkHelper),
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('financialaccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.financialaccount')),
                ('account_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='shomareh')),
                ('card_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='card')),
                ('shaba_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='shaba')),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.bank', verbose_name='bank')),
            ],
            options={
                'verbose_name': 'BankAccount',
                'verbose_name_plural': 'BankAccounts',
            },
            bases=('hesabyar.financialaccount',),
        ),
        migrations.CreateModel(
            name='Cheque',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.transaction')),
                ('cheque_date', models.DateField(verbose_name='تاریخ چک')),
            ],
            options={
                'verbose_name': 'چک',
                'verbose_name_plural': 'چک ها',
            },
            bases=('hesabyar.transaction', hesabyar.models.LinkHelper),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.transaction')),
                ('tax_percent', models.IntegerField(default=9, verbose_name='درصد مالیات')),
                ('invoice_datetime', models.DateTimeField(verbose_name='تاریخ فاکتور')),
                ('ship_fee', models.IntegerField(default=0, verbose_name='هزینه حمل')),
                ('discount', models.IntegerField(default=0, verbose_name='تخفیف')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
            bases=('hesabyar.transaction',),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('transaction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.transaction')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
            bases=('hesabyar.transaction',),
        ),
        migrations.CreateModel(
            name='ProductOrService',
            fields=[
                ('hesabyarpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.hesabyarpage')),
                ('unit_price', models.IntegerField(default=0, verbose_name='unit_price')),
                ('unit_name', models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته'), ('کیسه', 'کیسه'), ('شات', 'شات'), ('فنجان', 'فنجان'), ('جفت', 'جفت')], default='عدد', max_length=50, verbose_name='unit_name')),
            ],
            options={
                'verbose_name': 'ProductOrService',
                'verbose_name_plural': 'ProductOrServices',
            },
            bases=('hesabyar.hesabyarpage',),
        ),
        migrations.AddField(
            model_name='financialaccount',
            name='tags',
            field=models.ManyToManyField(blank=True, to='hesabyar.Tag', verbose_name='برچسب ها'),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('productorservice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.productorservice')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
            bases=('hesabyar.productorservice',),
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('productorservice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.productorservice')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
            },
            bases=('hesabyar.productorservice',),
        ),
        migrations.CreateModel(
            name='WareHouse',
            fields=[
                ('hesabyarpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.hesabyarpage')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='address')),
                ('tel', models.CharField(blank=True, max_length=50, null=True, verbose_name='tel')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.financialaccount', verbose_name='owner')),
            ],
            options={
                'verbose_name': 'WareHouse',
                'verbose_name_plural': 'WareHouses',
            },
            bases=('hesabyar.hesabyarpage',),
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('financialaccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.financialaccount')),
                ('logo_origin', models.ImageField(blank=True, null=True, upload_to='hesabyar/images/store/', verbose_name='logo')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='address')),
                ('tel', models.CharField(blank=True, max_length=50, null=True, verbose_name='tel')),
                ('bank_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='hesabyar.bankaccount', verbose_name='bankaccount')),
            ],
            options={
                'verbose_name': 'Store',
                'verbose_name_plural': 'Stores',
            },
            bases=('hesabyar.financialaccount', hesabyar.models.LinkHelper),
        ),
        migrations.CreateModel(
            name='InvoiceLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.IntegerField(verbose_name='row')),
                ('quantity', models.FloatField(verbose_name='quantity')),
                ('unit_price', models.IntegerField(verbose_name='unit_price')),
                ('unit_name', models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته'), ('کیسه', 'کیسه'), ('شات', 'شات'), ('فنجان', 'فنجان'), ('جفت', 'جفت')], default='عدد', max_length=50, verbose_name='unit_name')),
                ('description', models.CharField(blank=True, max_length=50, null=True, verbose_name='description')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.invoice', verbose_name='invoice')),
                ('productorservice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.productorservice', verbose_name='productorservice')),
            ],
            options={
                'verbose_name': 'InvoiceLine',
                'verbose_name_plural': 'InvoiceLines',
            },
        ),
        migrations.CreateModel(
            name='FinancialDocument',
            fields=[
                ('hesabyarpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.hesabyarpage')),
                ('bedehkar', models.IntegerField(default=0, verbose_name='bedehkar')),
                ('bestankar', models.IntegerField(default=0, verbose_name='bestankar')),
                ('document_datetime', models.DateTimeField(verbose_name='document_datetime')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.financialaccount', verbose_name='account')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.financialdocumentcategory', verbose_name='category')),
                ('financial_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.financialyear', verbose_name='financial_year')),
                ('transaction', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hesabyar.transaction', verbose_name='transaction')),
            ],
            options={
                'verbose_name': 'FinancialDocument',
                'verbose_name_plural': 'FinancialDocuments',
            },
            bases=('hesabyar.hesabyarpage',),
        ),
        migrations.CreateModel(
            name='WareHouseSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('date_registered', models.DateTimeField(verbose_name='date_registered')),
                ('quantity', models.IntegerField(verbose_name='quantity')),
                ('unit_name', models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته'), ('کیسه', 'کیسه'), ('شات', 'شات'), ('فنجان', 'فنجان'), ('جفت', 'جفت')], default='عدد', max_length=50, verbose_name='unit_name')),
                ('direction', models.CharField(choices=[('ورود به انبار', 'ورود به انبار'), ('خروج از انبار', 'خروج از انبار')], max_length=50, verbose_name='direction')),
                ('status', models.CharField(choices=[('تعریف اولیه', 'تعریف اولیه'), ('در جریان', 'در جریان'), ('تمام شده', 'تمام شده')], default='تعریف اولیه', max_length=50, verbose_name='status')),
                ('description', tinymce.models.HTMLField(blank=True, max_length=50000, null=True, verbose_name='description')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='creator')),
                ('ware_house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.warehouse', verbose_name='ware_house')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.product', verbose_name='product')),
            ],
            options={
                'verbose_name': 'WareHouseSheet',
                'verbose_name_plural': 'WareHouseSheets',
            },
            bases=(models.Model, hesabyar.models.LinkHelper),
        ),
    ]
