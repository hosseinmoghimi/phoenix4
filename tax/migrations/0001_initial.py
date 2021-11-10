# Generated by Django 3.2.2 on 2021-11-03 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0004_auto_20211103_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxPage',
            fields=[
                ('basicpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.basicpage')),
            ],
            options={
                'verbose_name': 'TaxPage',
                'verbose_name_plural': 'TaxPages',
            },
            bases=('core.basicpage',),
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('taxpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tax.taxpage')),
                ('year', models.IntegerField(verbose_name='سال')),
                ('amount', models.IntegerField(verbose_name='مبلغ')),
            ],
            options={
                'verbose_name': 'Tax',
                'verbose_name_plural': 'Taxes',
            },
            bases=('tax.taxpage',),
        ),
    ]
