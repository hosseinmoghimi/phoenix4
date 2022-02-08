# Generated by Django 3.2.2 on 2022-02-08 22:06

from django.db import migrations, models
import django.db.models.deletion
import hesabyar.models
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0004_profile_header_origin'),
        ('core', '0014_navlink_parent'),
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
                ('class_name', models.CharField(max_length=50, verbose_name='class_name')),
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
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('پرداخت نشده', 'پرداخت نشده'), ('کارتخوان', 'کارتخوان'), ('پرداخت نقدی', 'پرداخت نقدی')], default='پرداخت نشده', max_length=50, verbose_name='نحوه پرداخت')),
                ('status', models.CharField(choices=[('پیش فاکتور', 'پیش فاکتور'), ('در جریان', 'در جریان'), ('تحویل شده', 'تحویل شده')], default='پیش فاکتور', max_length=50, verbose_name='وضعیت')),
                ('tax_percent', models.IntegerField(default=9, verbose_name='درصد مالیات')),
                ('invoice_datetime', models.DateTimeField(verbose_name='تاریخ فاکتور')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('ship_fee', models.IntegerField(default=0, verbose_name='هزینه حمل')),
                ('discount', models.IntegerField(default=0, verbose_name='تخفیف')),
                ('description', tinymce.models.HTMLField(blank=True, max_length=50000, null=True, verbose_name='توضیحات')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
            bases=(models.Model, hesabyar.models.LinkHelper),
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
            name='ProductOrService',
            fields=[
                ('hesabyarpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.hesabyarpage')),
                ('unit_price', models.IntegerField(default=0, verbose_name='unit_price')),
                ('unit_name', models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته'), ('کیسه', 'کیسه'), ('شات', 'شات'), ('فنجان', 'فنجان')], default='عدد', max_length=50, verbose_name='unit_name')),
            ],
            options={
                'verbose_name': 'ProductOrService',
                'verbose_name_plural': 'ProductOrServices',
            },
            bases=('hesabyar.hesabyarpage',),
        ),
        migrations.CreateModel(
            name='ProfileFinancialAccount',
            fields=[
                ('financialaccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.financialaccount')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'ProfileFinancialAccount',
                'verbose_name_plural': 'ProfileFinancialAccounts',
            },
            bases=('hesabyar.financialaccount',),
        ),
        migrations.CreateModel(
            name='WareHouse',
            fields=[
                ('hesabyarpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.hesabyarpage')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='address')),
                ('tel', models.CharField(blank=True, max_length=50, null=True, verbose_name='tel')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.profilefinancialaccount', verbose_name='owner')),
            ],
            options={
                'verbose_name': 'WareHouse',
                'verbose_name_plural': 'WareHouses',
            },
            bases=('hesabyar.hesabyarpage',),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='پرداخت', max_length=50, verbose_name='title')),
                ('amount', models.IntegerField(verbose_name='amount')),
                ('date_paid', models.DateTimeField(verbose_name='date_paid')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='creator')),
                ('pay_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paid_set', to='hesabyar.financialaccount', verbose_name='pay_from')),
                ('pay_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_set', to='hesabyar.financialaccount', verbose_name='pay_to')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
            bases=(models.Model, hesabyar.models.LinkHelper),
        ),
        migrations.AddField(
            model_name='financialaccount',
            name='tags',
            field=models.ManyToManyField(blank=True, to='hesabyar.Tag', verbose_name='برچسب ها'),
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('profilefinancialaccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.profilefinancialaccount')),
                ('account_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='shomareh')),
                ('card_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='card')),
                ('shaba_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='shaba')),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.bank', verbose_name='bank')),
            ],
            options={
                'verbose_name': 'BankAccount',
                'verbose_name_plural': 'BankAccounts',
            },
            bases=('hesabyar.profilefinancialaccount',),
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
            name='Store',
            fields=[
                ('hesabyarpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.hesabyarpage')),
                ('logo_origin', models.ImageField(blank=True, null=True, upload_to='hesabyar/images/store/', verbose_name='logo')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='address')),
                ('tel', models.CharField(blank=True, max_length=50, null=True, verbose_name='tel')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.profilefinancialaccount', verbose_name='owner')),
                ('bank_account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stores', to='hesabyar.bankaccount', verbose_name='bankaccount')),
            ],
            options={
                'verbose_name': 'Store',
                'verbose_name_plural': 'Stores',
            },
            bases=('hesabyar.hesabyarpage',),
        ),
        migrations.CreateModel(
            name='InvoiceLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('row', models.IntegerField(verbose_name='row')),
                ('quantity', models.FloatField(verbose_name='quantity')),
                ('unit_price', models.IntegerField(verbose_name='unit_price')),
                ('unit_name', models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس'), ('بسته', 'بسته'), ('کیسه', 'کیسه'), ('شات', 'شات'), ('فنجان', 'فنجان')], default='عدد', max_length=50, verbose_name='unit_name')),
                ('description', models.CharField(blank=True, max_length=50, null=True, verbose_name='description')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.invoice', verbose_name='invoice')),
                ('productorservice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.productorservice', verbose_name='productorservice')),
            ],
            options={
                'verbose_name': 'InvoiceLine',
                'verbose_name_plural': 'InvoiceLines',
            },
        ),
        migrations.AddField(
            model_name='invoice',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hesabyar.profilefinancialaccount', verbose_name='مشتری'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.store', verbose_name='فروشنده'),
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
            ],
            options={
                'verbose_name': 'FinancialDocument',
                'verbose_name_plural': 'FinancialDocuments',
            },
            bases=('hesabyar.hesabyarpage',),
        ),
        migrations.CreateModel(
            name='Cheque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('cheque_date', models.DateField(verbose_name='تاریخ چک')),
                ('description', models.CharField(blank=True, max_length=50, null=True, verbose_name='توضیحات')),
                ('amount', models.IntegerField(default=0, verbose_name='مبلغ')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('status', models.CharField(choices=[('پیش نویس', 'پیش نویس'), ('برگشت خورده', 'برگشت خورده'), ('تسویه شده', 'تسویه شده')], default='پیش نویس', max_length=50, verbose_name='status')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cheque_owned', to='hesabyar.profilefinancialaccount', verbose_name='owner')),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cheque_received', to='hesabyar.profilefinancialaccount', verbose_name='receiver')),
            ],
            options={
                'verbose_name': 'چک',
                'verbose_name_plural': 'چک ها',
            },
            bases=(models.Model, hesabyar.models.LinkHelper),
        ),
        migrations.CreateModel(
            name='Cash',
            fields=[
                ('financialaccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.financialaccount')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.store', verbose_name='فروشگاه')),
            ],
            options={
                'verbose_name': 'Cash',
                'verbose_name_plural': 'Cashes',
            },
            bases=('hesabyar.financialaccount',),
        ),
        migrations.CreateModel(
            name='WareHouseSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('date_registered', models.DateTimeField(verbose_name='date_registered')),
                ('quantity', models.IntegerField(verbose_name='quantity')),
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
        migrations.CreateModel(
            name='PaymentFinancialDocument',
            fields=[
                ('financialdocument_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.financialdocument')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.payment', verbose_name='payment')),
            ],
            options={
                'verbose_name': 'PaymentFinancialDocument',
                'verbose_name_plural': 'PaymentFinancialDocuments',
            },
            bases=('hesabyar.financialdocument',),
        ),
        migrations.CreateModel(
            name='InvoiceFinancialDocument',
            fields=[
                ('financialdocument_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.financialdocument')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.invoice', verbose_name='invoice')),
            ],
            options={
                'verbose_name': 'InvoiceFinancialDocument',
                'verbose_name_plural': 'InvoiceFinancialDocuments',
            },
            bases=('hesabyar.financialdocument',),
        ),
    ]
