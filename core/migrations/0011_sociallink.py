# Generated by Django 3.2.2 on 2021-06-26 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_profile_enabled'),
        ('core', '0010_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('link_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.link')),
                ('app_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='اپلیکیشن')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'SocialLink',
                'verbose_name_plural': 'شبکه اجتماعی',
            },
            bases=('core.link',),
        ),
    ]