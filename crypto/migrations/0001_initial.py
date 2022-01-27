# Generated by Django 3.2.2 on 2022-01-22 02:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0014_navlink_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoPage',
            fields=[
                ('basicpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.basicpage')),
            ],
            bases=('core.basicpage',),
        ),
        migrations.CreateModel(
            name='CryptoToken',
            fields=[
                ('cryptopage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='crypto.cryptopage')),
            ],
            options={
                'verbose_name': 'CryptoToken',
                'verbose_name_plural': 'CryptoTokens',
            },
            bases=('crypto.cryptopage',),
        ),
    ]