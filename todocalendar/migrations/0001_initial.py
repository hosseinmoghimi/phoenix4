# Generated by Django 3.2.2 on 2021-10-01 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarPage',
            fields=[
                ('basicpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.basicpage')),
            ],
            bases=('core.basicpage',),
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('calendarpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='todocalendar.calendarpage')),
                ('appointment_date', models.DateTimeField(verbose_name='appointment_date')),
                ('location', models.CharField(blank=True, max_length=50, null=True, verbose_name='location')),
                ('persons', models.ManyToManyField(blank=True, to='authentication.Profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Appointment',
                'verbose_name_plural': 'Appointments',
            },
            bases=('todocalendar.calendarpage',),
        ),
    ]
