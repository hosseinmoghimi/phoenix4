# Generated by Django 3.2.2 on 2021-08-05 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_basicpage_sub_title'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('category', models.CharField(choices=[('گاو', 'گاو'), ('مرغ', 'مرغ'), ('گوسفند', 'گوسفند'), ('شترمرغ', 'شترمرغ'), ('بوقلمون', 'بوقلمون')], max_length=50, verbose_name='category')),
                ('tag', models.CharField(default='0000', max_length=50, verbose_name='تگ')),
                ('weight', models.FloatField(default=0, verbose_name='وزن')),
                ('enter_date', models.DateTimeField(verbose_name='enter_date')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='farm/images/animal/', verbose_name='image')),
                ('buy_price', models.IntegerField(default=0, verbose_name='قیمت خرید')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
            ],
            options={
                'verbose_name': 'دام',
                'verbose_name_plural': 'دام ها',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='farm_employee_set', to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
            },
        ),
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
            ],
            options={
                'verbose_name': 'Farm',
                'verbose_name_plural': 'Farms',
            },
        ),
        migrations.CreateModel(
            name='LiveStockPage',
            fields=[
                ('basicpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.basicpage')),
            ],
            options={
                'verbose_name': 'LiveStockPage',
                'verbose_name_plural': 'LiveStockPages',
            },
            bases=('core.basicpage',),
        ),
        migrations.CreateModel(
            name='Saloon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farm.farm', verbose_name='farm')),
            ],
            options={
                'verbose_name': 'Saloon',
                'verbose_name_plural': 'Saloons',
            },
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('livestockpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='farm.livestockpage')),
            ],
            options={
                'verbose_name': 'Drug',
                'verbose_name_plural': 'Drugs',
            },
            bases=('farm.livestockpage',),
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('livestockpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='farm.livestockpage')),
                ('unit_name', models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس')], default='کیلوگرم', max_length=50, verbose_name='unit_name')),
                ('unit_price', models.IntegerField(default=1000, verbose_name='unit_price')),
            ],
            options={
                'verbose_name': 'Food',
                'verbose_name_plural': 'Foods',
            },
            bases=('farm.livestockpage',),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='description')),
                ('animal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='farm.animal', verbose_name='animal')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='farm.employee', verbose_name='employee')),
                ('farm', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='farm.farm', verbose_name='farm')),
                ('saloon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='farm.saloon', verbose_name='saloon')),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
            },
        ),
        migrations.CreateModel(
            name='Koshtar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('koshtar_date', models.DateTimeField(verbose_name='koshtar_date')),
                ('Jegar_price', models.IntegerField(default=0, verbose_name='قیمت آلایش')),
                ('Kalle_pache_price', models.IntegerField(default=0, verbose_name='قیمت کله پاچه')),
                ('pust_price', models.IntegerField(default=0, verbose_name='قیمت پوست')),
                ('transport_fee', models.IntegerField(default=0, verbose_name='هزینه حمل')),
                ('koshtar_fee', models.IntegerField(default=0, verbose_name='هزینه کشتار')),
                ('lashe_price', models.IntegerField(default=0, verbose_name='قیمت لاشه')),
                ('lashe_weight', models.FloatField(default=0, verbose_name='وزن لاشه')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='farm.animal', verbose_name='animal')),
            ],
            options={
                'verbose_name': 'Koshtar',
                'verbose_name_plural': 'Koshtars',
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='farm_doctor_set', to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Doctor',
                'verbose_name_plural': 'Doctors',
            },
        ),
        migrations.CreateModel(
            name='Cost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان هزینه')),
                ('value', models.IntegerField(verbose_name='هزینه')),
                ('cost_date', models.DateTimeField(verbose_name='date_time')),
                ('category', models.CharField(choices=[('هزینه', 'هزینه'), ('آب', 'آب'), ('برق', 'برق'), ('گاز', 'گاز'), ('تلفن', 'تلفن'), ('اجاره', 'اجاره'), ('نگهبان', 'نگهبان'), ('ساختمانی', 'ساختمانی')], default='هزینه', max_length=50, verbose_name='category')),
                ('documents', models.ManyToManyField(blank=True, to='core.Document', verbose_name='documents')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farm.employee', verbose_name='employee')),
                ('saloon', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='farm.saloon', verbose_name='سالن')),
            ],
            options={
                'verbose_name': 'Cost',
                'verbose_name_plural': 'Costs',
            },
        ),
        migrations.CreateModel(
            name='AnimalInSaloon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('animal_price', models.IntegerField(default=0, verbose_name='price')),
                ('enter_date', models.DateTimeField(verbose_name='تاریخ ورود')),
                ('exit_date', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ خروج')),
                ('animal_weight', models.FloatField(default=0, verbose_name='weight')),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farm.animal', verbose_name='animal')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='farm.employee', verbose_name='employee')),
                ('saloon', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='farm.saloon', verbose_name='saloon')),
            ],
            options={
                'verbose_name': 'AnimalInSaloon',
                'verbose_name_plural': 'AnimalInSaloons',
            },
        ),
        migrations.CreateModel(
            name='SaloonFood',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='quantity')),
                ('unit_name', models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه'), ('سرویس', 'سرویس')], max_length=50, verbose_name='unit_name')),
                ('unit_price', models.IntegerField(verbose_name='قیمت واحد')),
                ('food_date', models.DateTimeField(verbose_name='food_date')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='farm.employee', verbose_name='employee')),
                ('saloon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farm.saloon', verbose_name='saloon')),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='farm.food', verbose_name='food')),
            ],
            options={
                'verbose_name': 'SaloonFood',
                'verbose_name_plural': 'SaloonFoods',
            },
        ),
    ]
