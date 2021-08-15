# Generated by Django 3.2.2 on 2021-08-15 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mafia', '0002_alter_game_god'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='god',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mafia.god', verbose_name='god'),
        ),
        migrations.AlterField(
            model_name='gamerole',
            name='player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mafia.player', verbose_name='player'),
        ),
        migrations.AlterField(
            model_name='gamerole',
            name='turn',
            field=models.IntegerField(default=20, verbose_name='نوبت'),
        ),
    ]
