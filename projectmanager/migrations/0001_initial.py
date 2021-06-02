# Generated by Django 3.2.2 on 2021-06-02 08:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pre_title', models.CharField(blank=True, max_length=50, null=True, verbose_name='pre_title')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('image_origin', models.ImageField(blank=True, null=True, upload_to='projectmanager/images/employer/', verbose_name='image')),
            ],
            options={
                'verbose_name': 'Employer',
                'verbose_name_plural': 'Employers',
            },
        ),
        migrations.CreateModel(
            name='MaterialRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='تعداد')),
                ('unit_name', models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه')], default='عدد', max_length=50, verbose_name='واحد')),
                ('unit_price', models.IntegerField(verbose_name='فی')),
                ('description', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='توضیحات')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ درخواست')),
                ('date_delivered', models.DateTimeField(blank=True, null=True, verbose_name='تاریخ درخواست')),
                ('status', models.CharField(choices=[('DEFAULT', 'DEFAULT'), ('تعریف اولیه در سیستم', 'تعریف اولیه در سیستم'), ('تحویل شده', 'تحویل شده'), ('در حال بررسی', 'در حال بررسی'), ('رد شده', 'رد شده'), ('پذیرفته شده', 'پذیرفته شده'), ('درخواست شده', 'درخواست شده'), ('در حال خرید', 'در حال خرید'), ('متعلق به کارفرما', 'متعلق به کارفرما')], default='درخواست شده', max_length=50, verbose_name='وضعیت')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='authentication.profile', verbose_name='تحویل گیرنده')),
            ],
            options={
                'verbose_name': 'درخواست متریال',
                'verbose_name_plural': 'درخواست های متریال',
            },
        ),
        migrations.CreateModel(
            name='ProjectManagerPage',
            fields=[
                ('basicpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.basicpage')),
            ],
            options={
                'verbose_name': 'ProjectManagerPage',
                'verbose_name_plural': 'ProjectManagerPage',
            },
            bases=('core.basicpage',),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('projectmanagerpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='projectmanager.projectmanagerpage')),
                ('unit_name', models.CharField(choices=[('عدد', 'عدد'), ('گرم', 'گرم'), ('کیلوگرم', 'کیلوگرم'), ('تن', 'تن'), ('متر', 'متر'), ('متر مربع', 'متر مربع'), ('متر مکعب', 'متر مکعب'), ('قطعه', 'قطعه'), ('شاخه', 'شاخه'), ('دستگاه', 'دستگاه')], default='عدد', max_length=50, verbose_name='unit_name')),
                ('unit_price', models.IntegerField(default=0, verbose_name='unit_price')),
            ],
            options={
                'verbose_name': 'Material',
                'verbose_name_plural': 'Materials',
            },
            bases=('projectmanager.projectmanagerpage',),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('projectmanagerpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='projectmanager.projectmanagerpage')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
            bases=('projectmanager.projectmanagerpage',),
        ),
        migrations.CreateModel(
            name='MaterialRequestSignature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='date_added')),
                ('description', models.CharField(max_length=200, verbose_name='description')),
                ('status', models.CharField(choices=[('DEFAULT', 'DEFAULT'), ('تحویل شده', 'تحویل شده'), ('در حال بررسی', 'درحال بررسی'), ('رد شده', 'ردشده'), ('پذیرفته شده', 'پذیرفته شده'), ('درحال خرید', 'درحال خرید'), ('درخواست شده', 'درخواست شده')], default='درخواست شده', max_length=200, verbose_name='status')),
                ('material_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.materialrequest', verbose_name='درخواست')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'امضای درخواست متریال',
                'verbose_name_plural': 'امضا های درخواست متریال',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.profile', verbose_name='profile')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
            },
        ),
        migrations.CreateModel(
            name='OrganizationUnit',
            fields=[
                ('projectmanagerpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='projectmanager.projectmanagerpage')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.employer', verbose_name='employer')),
            ],
            options={
                'verbose_name': 'OrganizationUnit',
                'verbose_name_plural': 'OrganizationUnits',
            },
            bases=('projectmanager.projectmanagerpage',),
        ),
        migrations.AddField(
            model_name='materialrequest',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='projectmanager.material', verbose_name='متریال'),
        ),
        migrations.AddField(
            model_name='materialrequest',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.project', verbose_name='پروژه'),
        ),
        migrations.CreateModel(
            name='EmployeeSpeciality',
            fields=[
                ('projectmanagerpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='projectmanager.projectmanagerpage')),
                ('max', models.IntegerField(verbose_name='max')),
                ('value', models.IntegerField(verbose_name='value')),
                ('percent', models.IntegerField(verbose_name='percent')),
                ('verified', models.BooleanField(default=False, verbose_name='verified')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.employee', verbose_name='employee')),
            ],
            options={
                'verbose_name': 'EmployeeSpeciality',
                'verbose_name_plural': 'EmployeeSpecialitys',
            },
            bases=('projectmanager.projectmanagerpage',),
        ),
        migrations.AddField(
            model_name='employee',
            name='organization_unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.organizationunit', verbose_name='organizationunit'),
        ),
    ]
