# Generated by Django 3.2.2 on 2021-06-01 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_profilecontact'),
        ('core', '0004_auto_20210601_0334'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('icon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.icon')),
                ('download_counter', models.IntegerField(default=0, verbose_name='تعداد دانلود')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
                ('file', models.FileField(blank=True, null=True, upload_to='core/Document', verbose_name='فایل ضمیمه')),
                ('mirror_link', models.CharField(blank=True, max_length=10000, null=True, verbose_name='آدرس بیرونی')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='افزوده شده در')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='اصلاح شده در')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='پروفایل')),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'اسناد',
            },
            bases=('core.icon',),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('icon_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.icon')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
                ('url', models.CharField(default='#', max_length=2000, verbose_name='آدرس لینک')),
                ('new_tab', models.BooleanField(default=False, verbose_name='در صفحه جدید باز شود؟')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='افزوده شده در')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='اصلاح شده در')),
                ('profile_adder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='پروفایل')),
            ],
            options={
                'verbose_name': 'Link',
                'verbose_name_plural': 'لینک ها',
            },
            bases=('core.icon',),
        ),
        migrations.CreateModel(
            name='PageLink',
            fields=[
                ('link_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.link')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='links', to='core.basicpage', verbose_name='page')),
            ],
            options={
                'verbose_name': 'لینک صفحات',
                'verbose_name_plural': 'لینک های صفحات',
            },
            bases=('core.link',),
        ),
        migrations.CreateModel(
            name='PageDocument',
            fields=[
                ('document_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.document')),
                ('page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='core.basicpage', verbose_name='page')),
            ],
            bases=('core.document',),
        ),
    ]
