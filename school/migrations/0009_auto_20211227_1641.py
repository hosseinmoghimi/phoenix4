# Generated by Django 3.2.2 on 2021-12-27 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0008_alter_attendance_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='time_added',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='time_added'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(choices=[('حاضر', 'حاضر'), ('غایب', 'غایب'), ('نا مشخص', 'نا مشخص'), ('تاخیر', 'تاخیر'), ('تشویق', 'تشویق'), ('تنبیه', 'تنبیه')], max_length=50, verbose_name='status'),
        ),
    ]
