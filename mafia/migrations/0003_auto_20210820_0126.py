# Generated by Django 3.2.2 on 2021-08-19 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mafia', '0002_gamerole_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gameday',
            options={'verbose_name': 'GameDay', 'verbose_name_plural': 'روزهای بازی'},
        ),
        migrations.AlterModelOptions(
            name='gamenight',
            options={'verbose_name': 'GameNight', 'verbose_name_plural': 'شب های بازی'},
        ),
        migrations.AlterModelOptions(
            name='gamerole',
            options={'verbose_name': 'GameRole', 'verbose_name_plural': 'نقش های بازی'},
        ),
        migrations.AddField(
            model_name='gameday',
            name='status',
            field=models.CharField(choices=[('در حال اجرا', 'در حال اجرا'), ('پایان یافته', 'پایان یافته')], default='sdsds', max_length=50, verbose_name='status'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gamenight',
            name='status',
            field=models.CharField(choices=[('در حال اجرا', 'در حال اجرا'), ('پایان یافته', 'پایان یافته')], default='sdsd', max_length=50, verbose_name='status'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='role',
            name='night_act_max',
            field=models.IntegerField(default=0, verbose_name='تعداد اکت شب'),
        ),
        migrations.AddField(
            model_name='role',
            name='night_act_title',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='عنوان اکت شب'),
        ),
        migrations.AlterField(
            model_name='gamerole',
            name='status',
            field=models.CharField(choices=[('زنده', 'زنده'), ('شات شده', 'شات شده'), ('اخراج شده', 'اخراج شده')], default='زنده', max_length=50, verbose_name='state'),
        ),
        migrations.CreateModel(
            name='NightAct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('acted_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='night_acted_set', to='mafia.gamerole', verbose_name='نقش')),
                ('actor_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='night_actor_set', to='mafia.gamerole', verbose_name='نقش فاعل')),
                ('night', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.gamenight', verbose_name='gamenight')),
            ],
            options={
                'verbose_name': 'NightShot',
                'verbose_name_plural': 'شات های شب',
            },
        ),
    ]
