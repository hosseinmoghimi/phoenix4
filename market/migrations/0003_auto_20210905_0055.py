# Generated by Django 3.2.2 on 2021-09-04 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_auto_20210904_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='old_price',
            field=models.IntegerField(default=0, verbose_name='قیمت قبلی'),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('marketpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='market.marketpage')),
                ('shops', models.ManyToManyField(to='market.Shop', verbose_name='shops')),
            ],
            options={
                'verbose_name': 'Offer',
                'verbose_name_plural': 'Offers',
            },
            bases=('market.marketpage',),
        ),
    ]
