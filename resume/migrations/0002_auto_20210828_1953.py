# Generated by Django 3.2.2 on 2021-08-28 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumefact',
            name='color',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='resumefact',
            name='icon',
            field=models.CharField(blank=True, choices=[('<i class="bx bxl-twitter"></i>', 'Twitter'), ('<i class="bx bxl-facebook"></i>', 'Facebook'), ('<i class="bx bxl-instagram"></i>', 'Instagram'), ('<i class="bx bxl-skype"></i>', 'Google Plus'), ('<i class="bx bxl-linkedin"></i>', 'Linkedin'), ('<i class="bi bi-journal-richtext"></i>', 'Journal'), ('<i class="bi bi-emoji-smile"></i>', 'Emoji'), ('<i class="bi bi-headset"></i>', 'Headset'), ('<i class="bi bi-award"></i>', 'Award')], max_length=100, null=True, verbose_name='icon'),
        ),
        migrations.AlterField(
            model_name='resumesociallink',
            name='icon',
            field=models.CharField(choices=[('<i class="bx bxl-twitter"></i>', 'Twitter'), ('<i class="bx bxl-facebook"></i>', 'Facebook'), ('<i class="bx bxl-instagram"></i>', 'Instagram'), ('<i class="bx bxl-skype"></i>', 'Google Plus'), ('<i class="bx bxl-linkedin"></i>', 'Linkedin'), ('<i class="bi bi-journal-richtext"></i>', 'Journal'), ('<i class="bi bi-emoji-smile"></i>', 'Emoji'), ('<i class="bi bi-headset"></i>', 'Headset'), ('<i class="bi bi-award"></i>', 'Award')], max_length=50, verbose_name='icon'),
        ),
    ]
