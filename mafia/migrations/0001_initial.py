# Generated by Django 3.2.2 on 2021-10-01 12:22

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(verbose_name='start_date')),
                ('scenario', models.CharField(choices=[('تفنگ دار', 'تفنگ دار'), ('گروگان گیر', 'گروگان گیر'), ('مذاکره', 'مذاکره'), ('دانش آموز', 'دانش آموز'), ('روح', 'روح')], max_length=50, verbose_name='scenario')),
                ('status', models.CharField(choices=[('در حال ساخت', 'در حال ساخت'), ('در حال نقش دهی', 'در حال نقش دهی'), ('معارفه', 'معارفه'), ('در حال اجرا', 'در حال اجرا'), ('بازی در فاز روز', 'بازی در فاز روز'), ('رای گیری برای ورود به دادگاه', 'رای گیری برای ورود به دادگاه'), ('رای گیری برای خروج از شهر', 'رای گیری برای خروج از شهر'), ('بازی در فاز شب', 'بازی در فاز شب'), ('تمام شده', 'تمام شده')], max_length=50, verbose_name='وضعیت بازی')),
            ],
            options={
                'verbose_name': 'Game',
                'verbose_name_plural': 'Games',
            },
        ),
        migrations.CreateModel(
            name='GameDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counter', models.IntegerField(verbose_name='شماره روز')),
                ('status', models.CharField(choices=[('در حال اجرا', 'در حال اجرا'), ('پایان یافته', 'پایان یافته')], max_length=50, verbose_name='status')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.game', verbose_name='بازی')),
            ],
            options={
                'verbose_name': 'GameDay',
                'verbose_name_plural': 'روزهای بازی',
            },
        ),
        migrations.CreateModel(
            name='GameNight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counter', models.IntegerField(verbose_name='شماره شب')),
                ('status', models.CharField(choices=[('در حال اجرا', 'در حال اجرا'), ('پایان یافته', 'پایان یافته')], max_length=50, verbose_name='وضعیت')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.game', verbose_name='بازی')),
            ],
            options={
                'verbose_name': 'GameNight',
                'verbose_name_plural': 'شب های بازی',
            },
        ),
        migrations.CreateModel(
            name='GameRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turn', models.IntegerField(default=20, verbose_name='نوبت')),
                ('status', models.CharField(choices=[('زنده', 'زنده'), ('شات شده', 'شات شده'), ('اخراج شده', 'اخراج شده')], default='زنده', max_length=50, verbose_name='state')),
                ('description', models.CharField(blank=True, max_length=50, null=True, verbose_name='description')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.game', verbose_name='Game')),
            ],
            options={
                'verbose_name': 'GameRole',
                'verbose_name_plural': 'نقش های بازی',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='mafia/images/role/', verbose_name='image')),
                ('priority', models.IntegerField(default=100, verbose_name='ترتیب')),
                ('side', models.CharField(choices=[('مافیا', 'مافیا'), ('شهروند', 'شهروند')], max_length=50, verbose_name='side')),
                ('role_name', models.CharField(max_length=50, verbose_name='role')),
                ('default_count', models.IntegerField(default=0, verbose_name='default')),
                ('night_act_title', models.CharField(blank=True, max_length=50, null=True, verbose_name='عنوان اکت شب')),
                ('night_act_max', models.IntegerField(default=0, verbose_name='تعداد اکت شب')),
                ('description', tinymce.models.HTMLField(blank=True, null=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('level', models.CharField(choices=[('ورود به دادگاه', 'ورود به دادگاه'), ('خروج از شهر', 'خروج از شهر')], default='ورود به دادگاه', max_length=50, verbose_name='مرحله')),
                ('accused', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voteaccused_set', to='mafia.gamerole', verbose_name='متهم')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.gameday', verbose_name='روز بازی')),
                ('voter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='voter_set', to='mafia.gamerole', verbose_name='رای دهنده')),
            ],
            options={
                'verbose_name': 'Vote',
                'verbose_name_plural': 'Votes',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0, verbose_name='score')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Player',
                'verbose_name_plural': 'Players',
            },
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
        migrations.CreateModel(
            name='God',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0, verbose_name='score')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'God',
                'verbose_name_plural': 'Gods',
            },
        ),
        migrations.AddField(
            model_name='gamerole',
            name='player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mafia.player', verbose_name='player'),
        ),
        migrations.AddField(
            model_name='gamerole',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.role', verbose_name='role'),
        ),
        migrations.AddField(
            model_name='game',
            name='god',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mafia.god', verbose_name='god'),
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='description')),
                ('night', models.IntegerField(verbose_name='night?')),
                ('role_block', models.BooleanField(default=False, verbose_name='role_block')),
                ('action_target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_target_set', to='mafia.gamerole', verbose_name='role2')),
                ('game_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='action_doer_set', to='mafia.gamerole', verbose_name='role1')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='Accused',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votes_count', models.IntegerField(verbose_name='تعداد رای های خروج')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.gameday', verbose_name='روز بازی')),
                ('game_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mafia.gamerole', verbose_name='بازیکن')),
            ],
            options={
                'verbose_name': 'Accused',
                'verbose_name_plural': 'Accuseds',
            },
        ),
    ]
