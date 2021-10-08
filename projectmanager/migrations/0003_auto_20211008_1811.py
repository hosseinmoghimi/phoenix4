# Generated by Django 3.2.2 on 2021-10-08 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projectmanager', '0002_auto_20211003_0130'),
    ]

    operations = [
        migrations.CreateModel(
            name='WareHouse',
            fields=[
                ('organizationunit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='projectmanager.organizationunit')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس')),
            ],
            options={
                'verbose_name': 'WareHouse',
                'verbose_name_plural': 'WareHouses',
            },
            bases=('projectmanager.organizationunit',),
        ),
        migrations.CreateModel(
            name='WareHouseSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.CharField(choices=[('ورود به انبار', 'ورود به انبار'), ('خروج از انبار', 'خروج از انبار')], max_length=50, verbose_name='direction')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('date_imported', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ ورود')),
                ('date_exported', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ خروج')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='description')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='warehousesheets_created', to='projectmanager.employee', verbose_name='ثبت کننده')),
                ('tahvil_dahandeh', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='warehousesheets_importer', to='projectmanager.employee', verbose_name='تحویل دهنده')),
                ('tahvil_girandeh', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='warehousesheets_exporter', to='projectmanager.employee', verbose_name='تحویل گیرنده')),
                ('ware_house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.warehouse', verbose_name='warehouse')),
            ],
            options={
                'verbose_name': 'WareHouseSheet',
                'verbose_name_plural': 'WareHouseSheets',
            },
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('DEFAULT', 'DEFAULT'), ('تعریف اولیه در سیستم', 'تعریف اولیه در سیستم'), ('تحویل شده', 'تحویل شده'), ('در حال انجام', 'در حال انجام'), ('رد شده', 'رد شده'), ('پذیرفته شده', 'پذیرفته شده'), ('درخواست شده', 'درخواست شده'), ('در حال خرید', 'در حال خرید'), ('متعلق به کارفرما', 'متعلق به کارفرما'), ('موجود در انبار', 'موجود در انبار')], default='درخواست شده', max_length=50, verbose_name='وضعیت'),
        ),
        migrations.CreateModel(
            name='WareHouseExportSheet',
            fields=[
                ('warehousesheet_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='projectmanager.warehousesheet')),
            ],
            options={
                'verbose_name': 'WareHouseImportSheet',
                'verbose_name_plural': 'WareHouseImportSheets',
            },
            bases=('projectmanager.warehousesheet',),
        ),
        migrations.CreateModel(
            name='WareHouseImportSheet',
            fields=[
                ('warehousesheet_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='projectmanager.warehousesheet')),
            ],
            options={
                'verbose_name': 'WareHouseImportSheet',
                'verbose_name_plural': 'WareHouseImportSheets',
            },
            bases=('projectmanager.warehousesheet',),
        ),
        migrations.CreateModel(
            name='WareHouseSheetLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='quantity')),
                ('serial_no', models.CharField(blank=True, max_length=50, null=True, verbose_name='serial_no')),
                ('unit_name', models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس')], max_length=50, verbose_name='unit_name')),
                ('unit_price', models.IntegerField(blank=True, null=True, verbose_name='unit_price')),
                ('location', models.CharField(blank=True, max_length=50, null=True, verbose_name='location')),
                ('shelf', models.IntegerField(blank=True, null=True, verbose_name='کمد')),
                ('row', models.IntegerField(blank=True, null=True, verbose_name='طبقه')),
                ('col', models.IntegerField(blank=True, null=True, verbose_name='ردیف')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='description')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.material', verbose_name='material')),
                ('ware_house_sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.warehousesheet', verbose_name='warehousesheet')),
            ],
            options={
                'verbose_name': 'WareHouseSheetLine',
                'verbose_name_plural': 'WareHouseSheetLines',
            },
        ),
        migrations.CreateModel(
            name='WareHouseMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=50, null=True, verbose_name='کد')),
                ('minimum', models.IntegerField(default=0, verbose_name='minimum')),
                ('order_point', models.IntegerField(default=0, verbose_name='order_point')),
                ('unit_name', models.CharField(blank=True, choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس')], max_length=50, null=True, verbose_name='unit_name')),
                ('unit_price', models.IntegerField(blank=True, null=True, verbose_name='unit_price')),
                ('shelf', models.CharField(blank=True, max_length=50, null=True, verbose_name='کمد')),
                ('row', models.CharField(blank=True, max_length=50, null=True, verbose_name='طبقه')),
                ('col', models.CharField(blank=True, max_length=50, null=True, verbose_name='ردیف')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='description')),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.material', verbose_name='material')),
                ('ware_house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.warehouse', verbose_name='warehouse')),
            ],
            options={
                'verbose_name': 'WareHouseMaterial',
                'verbose_name_plural': 'WareHouseMaterials',
            },
        ),
    ]
