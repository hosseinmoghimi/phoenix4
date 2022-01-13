# Generated by Django 3.2.2 on 2022-01-13 23:41

from django.db import migrations, models


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
                ('app_name', models.CharField(max_length=50, verbose_name='app_name')),
            ],
            options={
                'verbose_name': 'MembershipRequest',
                'verbose_name_plural': 'MembershipRequests',
            },
        ),
    ]
