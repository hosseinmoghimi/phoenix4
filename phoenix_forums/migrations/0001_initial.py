# Generated by Django 3.2.2 on 2021-10-01 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumsPage',
            fields=[
                ('basicpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.basicpage')),
            ],
            bases=('core.basicpage',),
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('forumspage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='phoenix_forums.forumspage')),
            ],
            options={
                'verbose_name': 'Forum',
                'verbose_name_plural': 'Forums',
            },
            bases=('phoenix_forums.forumspage',),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('forumspage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='phoenix_forums.forumspage')),
                ('post_forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='phoenix_forums.forum', verbose_name='forum')),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Post',
            },
            bases=('phoenix_forums.forumspage',),
        ),
    ]
