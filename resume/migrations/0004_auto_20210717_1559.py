# Generated by Django 3.2.2 on 2021-07-17 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0003_auto_20210717_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumefact',
            name='icon',
            field=models.CharField(choices=[('<i class="bx bxl-twitter"></i>', 'Twitter'), ('<i class="bx bxl-facebook"></i>', 'Facebook'), ('<i class="bx bxl-instagram"></i>', 'Instagram'), ('<i class="bx bxl-skype"></i>', 'Google Plus'), ('<i class="bx bxl-linkedin"></i>', 'Linkedin')], max_length=100, verbose_name='icon'),
        ),
        migrations.CreateModel(
            name='ResumeSocialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('href', models.CharField(max_length=5000, verbose_name='href')),
                ('link_class', models.CharField(choices=[('twitter', 'Twitter'), ('facebook', 'Facebook'), ('instagram', 'Instagram'), ('skype', 'Google Plus'), ('linkedin', 'Linkedin')], max_length=50, verbose_name='link_class')),
                ('icon', models.CharField(choices=[('<i class="bx bxl-twitter"></i>', 'Twitter'), ('<i class="bx bxl-facebook"></i>', 'Facebook'), ('<i class="bx bxl-instagram"></i>', 'Instagram'), ('<i class="bx bxl-skype"></i>', 'Google Plus'), ('<i class="bx bxl-linkedin"></i>', 'Linkedin')], max_length=50, verbose_name='icon')),
                ('resume_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.resumeindex', verbose_name='resumeindex')),
            ],
            options={
                'verbose_name': 'ResumeSocialLink',
                'verbose_name_plural': 'ResumeSocialLinks',
            },
        ),
    ]
