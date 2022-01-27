# Generated by Django 3.2.2 on 2022-01-27 02:25

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0003_auto_20220127_0535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumeindex',
            name='facts_top',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='facts_top'),
        ),
        migrations.AlterField(
            model_name='resumeindex',
            name='skills_top',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='skills_top'),
        ),
    ]