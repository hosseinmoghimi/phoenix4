# Generated by Django 3.2.2 on 2021-11-09 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0007_alter_document_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryPage',
            fields=[
                ('basicpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.basicpage')),
            ],
            options={
                'verbose_name': 'TaxPage',
                'verbose_name_plural': 'TaxPages',
            },
            bases=('core.basicpage',),
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('librarypage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='library.librarypage')),
                ('price', models.IntegerField(verbose_name='price')),
                ('year', models.IntegerField(verbose_name='year')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
            bases=('library.librarypage',),
        ),
    ]