# Generated by Django 3.2.2 on 2021-07-16 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50, verbose_name='نام کامل')),
                ('mobile', models.CharField(max_length=50, verbose_name='شماره تماس')),
                ('email', models.EmailField(max_length=254, verbose_name='ایمیل')),
                ('subject', models.CharField(max_length=50, verbose_name='عنوان پیام')),
                ('message', models.CharField(max_length=50, verbose_name='متن پیام')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='افزوده شده در')),
                ('resume_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.resumeindex', verbose_name='resume')),
            ],
            options={
                'verbose_name': 'ContactMessage',
                'verbose_name_plural': 'پیام های ارتباط با ما',
            },
        ),
    ]
