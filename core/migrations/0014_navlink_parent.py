# Generated by Django 3.2.2 on 2022-01-21 23:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_remove_basicpage_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='navlink',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.navlink', verbose_name='navlink'),
        ),
    ]
