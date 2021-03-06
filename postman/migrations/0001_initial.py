# Generated by Django 3.2.2 on 2022-01-06 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projectmanager', '0015_auto_20211209_1930'),
        ('authentication', '0001_initial'),
        ('core', '0013_remove_basicpage_keywords'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostmanPage',
            fields=[
                ('basicpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.basicpage')),
            ],
            options={
                'verbose_name': 'PostmanPage',
                'verbose_name_plural': 'PostmanPages',
            },
            bases=('core.basicpage',),
        ),
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('postmanpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='postman.postmanpage')),
            ],
            options={
                'verbose_name': 'Letter',
                'verbose_name_plural': 'Letters',
            },
            bases=('postman.postmanpage',),
        ),
        migrations.CreateModel(
            name='LetterSignature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('description', models.CharField(max_length=200, verbose_name='description')),
                ('status', models.CharField(choices=[('DEFAULT', 'DEFAULT'), ('تحویل شده', 'تحویل شده'), ('در حال بررسی', 'درحال بررسی')], default='DEFAULT', max_length=200, verbose_name='status')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='authentication.profile', verbose_name='profile')),
                ('letter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postman.letter', verbose_name='letter')),
            ],
            options={
                'verbose_name': 'LetterSignature',
                'verbose_name_plural': 'LetterSignatures',
            },
        ),
        migrations.CreateModel(
            name='LetterPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_sent', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='letters_received', to='projectmanager.organizationunit', verbose_name='receiver')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='letters_send', to='projectmanager.organizationunit', verbose_name='sender')),
                ('letter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='postman.letter', verbose_name='letter')),
            ],
            options={
                'verbose_name': 'LetterPosition',
                'verbose_name_plural': 'LetterPositions',
            },
        ),
    ]
