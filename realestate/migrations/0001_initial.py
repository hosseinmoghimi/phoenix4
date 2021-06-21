# Generated by Django 3.2.2 on 2021-06-21 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('floor', models.CharField(choices=[('زیر زمین', 'زیر زمین'), ('همکف', 'همکف'), ('اول', 'اول'), ('دوم', 'دوم'), ('سوم', 'سوم'), ('چهارم', 'چهارم')], default='همکف', max_length=50, verbose_name='طبقه')),
                ('parking', models.BooleanField(default=False, verbose_name='پارکینگ دارد؟')),
                ('elevator', models.BooleanField(default=False, verbose_name='آسانسور دارد؟')),
                ('bedrooms', models.IntegerField(verbose_name='تعداد خواب')),
                ('kitchen_type', models.CharField(choices=[('معمولی', 'معمولی'), ('جزیره', 'جزیره')], default='معمولی', max_length=50, verbose_name='نوع آشپزخانه')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='توضیحات')),
            ],
            options={
                'verbose_name': 'Property',
                'verbose_name_plural': 'Propertys',
            },
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
    ]
