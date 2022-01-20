# Generated by Django 3.2.2 on 2022-01-11 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projectmanager', '0015_auto_20211209_1930'),
        ('authentication', '0001_initial'),
        ('core', '0013_remove_basicpage_keywords'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='عنوان')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='address')),
                ('tel', models.CharField(blank=True, max_length=50, null=True, verbose_name='tel')),
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
            ],
            options={
                'verbose_name': 'FinancialDocument',
                'verbose_name_plural': 'FinancialDocuments',
            },
        ),
        migrations.CreateModel(
            name='FinancialYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
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
            name='Cash',
            fields=[
                ('financialaccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.financialaccount')),
            ],
            options={
                'verbose_name': 'Cash',
                'verbose_name_plural': 'Cashes',
            },
            bases=('hesabyar.financialaccount',),
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
            name='FinancialDocument',
            fields=[
                ('hesabyarpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.hesabyarpage')),
                ('bedehkar', models.IntegerField(default=0, verbose_name='bedehkar')),
                ('bestankar', models.IntegerField(default=0, verbose_name='bestankar')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.financialaccount', verbose_name='account')),
                ('financial_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.financialyear', verbose_name='financial_year')),
            ],
            options={
                'verbose_name': 'FinancialDocument',
                'verbose_name_plural': 'FinancialDocuments',
            },
            bases=('hesabyar.hesabyarpage',),
        ),
        migrations.CreateModel(
            name='EmployerFinancialAccount',
            fields=[
                ('financialaccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.financialaccount')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.employer', verbose_name='employer')),
            ],
            options={
                'verbose_name': 'EmployerFinancialAccount',
                'verbose_name_plural': 'EmployerFinancialAccounts',
            },
            bases=('hesabyar.financialaccount',),
        ),
        migrations.CreateModel(
            name='BankAccount',
            fields=[
                ('profilefinancialaccount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='hesabyar.profilefinancialaccount')),
                ('branch', models.CharField(blank=True, max_length=50, null=True, verbose_name='branch')),
                ('shomare', models.CharField(blank=True, max_length=50, null=True, verbose_name='shomareh')),
                ('card', models.CharField(blank=True, max_length=50, null=True, verbose_name='card')),
                ('shaba', models.CharField(blank=True, max_length=50, null=True, verbose_name='shaba')),
                ('bank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hesabyar.bank', verbose_name='bank')),
            ],
            options={
                'verbose_name': 'BankAccount',
                'verbose_name_plural': 'BankAccounts',
            },
            bases=('hesabyar.profilefinancialaccount',),
        ),
    ]