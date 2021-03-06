# Generated by Django 3.2.2 on 2022-01-15 08:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=50, verbose_name='mobile')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('read', models.BooleanField(default=False, verbose_name='read?')),
                ('handled', models.BooleanField(default=False, verbose_name='handled?')),
                ('date_handled', models.DateTimeField(blank=True, null=True, verbose_name='date_handled')),
                ('app_name', models.CharField(max_length=50, verbose_name='app_name')),
                ('handled_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'MembershipRequest',
                'verbose_name_plural': 'MembershipRequests',
            },
        ),
    ]
