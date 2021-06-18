# Generated by Django 3.2.2 on 2021-06-13 01:47

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_profile_enabled'),
        ('core', '0003_auto_20210611_1645'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', tinymce.models.HTMLField(verbose_name='comment')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.basicpage', verbose_name='page')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
        ),
    ]