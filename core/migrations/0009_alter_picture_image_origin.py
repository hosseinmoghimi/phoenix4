# Generated by Django 3.2.2 on 2021-12-03 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_document_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='image_origin',
            field=models.ImageField(blank=True, null=True, upload_to='core/images/picture/', verbose_name='image'),
        ),
    ]
