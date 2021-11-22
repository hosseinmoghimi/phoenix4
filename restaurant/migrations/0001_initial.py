# Generated by Django 3.2.2 on 2021-11-22 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('core', '0007_alter_document_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Guest',
                'verbose_name_plural': 'Guests',
            },
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Host',
                'verbose_name_plural': 'Hosts',
            },
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('date_served', models.DateField(verbose_name='date_served')),
                ('meal_type', models.CharField(choices=[('صبحانه', 'صبحانه'), ('ناهار', 'ناهار'), ('شام', 'شام')], max_length=50, verbose_name='meal type')),
                ('reserved', models.BooleanField(default=False, verbose_name='reserved')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.host', verbose_name='host')),
            ],
            options={
                'verbose_name': 'Meal',
                'verbose_name_plural': 'Meals',
            },
        ),
        migrations.CreateModel(
            name='RestaurantPage',
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
            name='Food',
            fields=[
                ('restaurantpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='restaurant.restaurantpage')),
                ('callery', models.IntegerField(default=0, verbose_name='کالری')),
                ('fat', models.IntegerField(default=0, verbose_name='چربی')),
                ('sugar', models.IntegerField(default=0, verbose_name='قند')),
                ('carbo_hydrathe', models.IntegerField(default=0, verbose_name='کربو هیدرات')),
                ('salt', models.IntegerField(default=0, verbose_name='نمک')),
                ('protein', models.IntegerField(default=0, verbose_name='پروتئین')),
                ('fat_acid', models.IntegerField(default=0, verbose_name='اسید چرب')),
            ],
            options={
                'verbose_name': 'Food',
                'verbose_name_plural': 'Foods',
            },
            bases=('restaurant.restaurantpage',),
        ),
        migrations.CreateModel(
            name='ReservedMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='تعداد')),
                ('date_reserved', models.DateTimeField(auto_now_add=True, verbose_name='date_reserved')),
                ('date_served', models.DateTimeField(blank=True, null=True, verbose_name='date_served')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.guest', verbose_name='guest')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.meal', verbose_name='meal')),
            ],
            options={
                'verbose_name': 'ReservedMeal',
                'verbose_name_plural': 'ReservedMeals',
            },
        ),
        migrations.AddField(
            model_name='meal',
            name='foods',
            field=models.ManyToManyField(to='restaurant.Food', verbose_name='food'),
        ),
    ]
