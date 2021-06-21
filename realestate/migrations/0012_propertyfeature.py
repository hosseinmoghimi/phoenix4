# Generated by Django 3.2.2 on 2021-06-21 21:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('realestate', '0011_property_date_added'),
    ]

    operations = [
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
