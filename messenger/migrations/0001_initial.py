# Generated by Django 3.2.2 on 2021-06-13 01:47

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0004_pagecomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessengerPage',
            fields=[
                ('basicpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.basicpage')),
            ],
            bases=('core.basicpage',),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('messengerpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='messenger.messengerpage')),
                ('read', models.BooleanField(default=False, verbose_name='read?')),
                ('draft', models.BooleanField(default=True, verbose_name='draft?')),
                ('slogan', models.TextField(blank=True, null=True, verbose_name='short_description')),
                ('body', tinymce.models.HTMLField(blank=True, null=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
            bases=('messenger.messengerpage',),
        ),
    ]
