# Generated by Django 3.2.2 on 2022-02-08 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0008_remove_testimonial_image_origin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonial',
            name='body',
            field=models.TextField(blank=True, max_length=20000, null=True, verbose_name='متن'),
        ),
    ]
