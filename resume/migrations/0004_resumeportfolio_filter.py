# Generated by Django 3.2.2 on 2021-06-26 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0003_auto_20210627_0235'),
    ]

    operations = [
        migrations.AddField(
            model_name='resumeportfolio',
            name='filter',
            field=models.CharField(choices=[('app', 'app'), ('card', 'card'), ('web', 'web')], default='web', max_length=50, verbose_name='filter'),
        ),
    ]