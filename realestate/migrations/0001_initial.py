# Generated by Django 3.2.2 on 2021-07-02 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounting', '0002_auto_20210702_1625'),
        ('authentication', '0002_profile_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('asset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.asset')),
                ('brand', models.CharField(choices=[('پژو', 'پژو'), ('ایران خودرو', 'ایران خودرو'), ('سایپا', 'سایپا')], max_length=50, verbose_name='brand')),
                ('product', models.CharField(max_length=50, verbose_name='محصول')),
                ('color', models.CharField(max_length=50, verbose_name='رنگ')),
                ('distance', models.IntegerField(verbose_name='کارکرد به کیلومتر')),
            ],
            options={
                'verbose_name': 'Car',
                'verbose_name_plural': 'Cars',
            },
            bases=('accounting.asset',),
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('asset_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='accounting.asset')),
                ('floor', models.CharField(choices=[('زیر زمین', 'زیر زمین'), ('همکف', 'همکف'), ('اول', 'اول'), ('دوم', 'دوم'), ('سوم', 'سوم'), ('چهارم', 'چهارم')], default='همکف', max_length=50, verbose_name='طبقه')),
                ('garage', models.IntegerField(default=0, verbose_name='تعداد گاراژ')),
                ('elevator', models.BooleanField(default=False, verbose_name='آسانسور دارد؟')),
                ('bed_rooms', models.IntegerField(default=1, verbose_name='تعداد خواب')),
                ('bath_rooms', models.IntegerField(default=1, verbose_name='تعداد سرویس بهداشتی')),
                ('kitchen_type', models.CharField(choices=[('معمولی', 'معمولی'), ('جزیره', 'جزیره')], default='معمولی', max_length=50, verbose_name='نوع آشپزخانه')),
                ('area', models.IntegerField(verbose_name='مساحت')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='آدرس')),
                ('location', models.CharField(blank=True, max_length=5000, null=True, verbose_name='location')),
                ('agent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='مسئول فروش')),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Propertys',
            },
            bases=('accounting.asset',),
        ),
        migrations.CreateModel(
            name='PropertyMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='realestate/media/property', verbose_name='file')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestate.property', verbose_name='ملک')),
            ],
            options={
                'verbose_name': 'PropertyMedia',
                'verbose_name_plural': 'PropertyMedias',
            },
        ),
        migrations.CreateModel(
            name='PropertyFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('value', models.CharField(max_length=50, verbose_name='value')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='realestate.property', verbose_name='ملک')),
            ],
            options={
                'verbose_name': 'PropertyFeature',
                'verbose_name_plural': 'PropertyFeatures',
            },
        ),
    ]
