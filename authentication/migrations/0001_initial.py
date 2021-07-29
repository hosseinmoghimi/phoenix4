# Generated by Django 3.2.2 on 2021-07-28 09:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current', models.BooleanField(default=True, verbose_name='current')),
                ('mobile', models.CharField(blank=True, max_length=50, null=True, verbose_name='mobile')),
                ('bio', models.CharField(blank=True, max_length=50, null=True, verbose_name='bio')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='address')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='authentication/images/profile/', verbose_name='image')),
                ('enabled', models.BooleanField(default=True, verbose_name='enabled')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='ProfileContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('value', models.CharField(max_length=50, verbose_name='value')),
                ('icon', models.CharField(blank=True, max_length=50, null=True, verbose_name='icon')),
                ('bs_class', models.CharField(blank=True, max_length=50, null=True, verbose_name='bootstrap class')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'ProfileContact',
                'verbose_name_plural': 'ProfileContacts',
            },
        ),
    ]
