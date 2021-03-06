# Generated by Django 3.2.2 on 2021-11-08 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'verbose_name': 'لوکیشن', 'verbose_name_plural': 'لوکیشن ها'},
        ),
        migrations.AddField(
            model_name='location',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='maplocation_set', to='authentication.profile', verbose_name='profile'),
        ),
        migrations.AddField(
            model_name='location',
            name='location',
            field=models.CharField(default='wewewew', max_length=1000, verbose_name='لوکیشن'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='عنوان نقطه'),
        ),
    ]
