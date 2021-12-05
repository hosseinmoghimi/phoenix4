# Generated by Django 3.2.2 on 2021-12-05 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0009_alter_picture_image_origin'),
        ('projectmanager', '0012_auto_20211206_0145'),
        ('map', '0003_alter_location_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeSalary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(verbose_name='سال')),
                ('month', models.IntegerField(verbose_name='ماه')),
                ('month_name', models.CharField(max_length=50, verbose_name='ماه')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('date_paid', models.DateTimeField(verbose_name='تاریخ واریز')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.employee', verbose_name='employee')),
            ],
            options={
                'verbose_name': 'EmployeeSalary',
                'verbose_name_plural': 'EmployeeSalarys',
            },
        ),
        migrations.CreateModel(
            name='SalaryPage',
            fields=[
                ('basicpage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.basicpage')),
            ],
            bases=('core.basicpage',),
        ),
        migrations.CreateModel(
            name='WorkSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='map.location', verbose_name='location')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='salary.worksite', verbose_name='والد')),
            ],
            options={
                'verbose_name': 'WorkSite',
                'verbose_name_plural': 'WorkSites',
            },
        ),
        migrations.CreateModel(
            name='WorkGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('employees_origin', models.ManyToManyField(blank=True, to='projectmanager.Employee', verbose_name='employees')),
                ('organization_units', models.ManyToManyField(blank=True, to='projectmanager.OrganizationUnit', verbose_name='واحد های سازمانی')),
            ],
            options={
                'verbose_name': 'WorkGroup',
                'verbose_name_plural': 'WorkGroups',
            },
        ),
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_date', models.DateField(verbose_name='روز')),
                ('work_start', models.TimeField(verbose_name='ورود')),
                ('work_end', models.TimeField(verbose_name='خروج')),
                ('work_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salary.workgroup', verbose_name='گروه کاری')),
                ('work_site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='salary.worksite', verbose_name='محل کار')),
            ],
            options={
                'verbose_name': 'WorkDay',
                'verbose_name_plural': 'WorkDays',
            },
        ),
        migrations.CreateModel(
            name='SalaryLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.CharField(choices=[('مزایا', 'مزایا'), ('کسورات', 'کسورات')], default='مزایا', max_length=50, verbose_name='جهت')),
                ('title', models.CharField(choices=[('حقوق پایه', 'حقوق پایه'), ('حق فرزند', 'حق فرزند'), ('حق همسر', 'حق همسر'), ('بدی آب و هوا', 'بدی آب و هوا'), ('مالیات', 'مالیات')], max_length=50, verbose_name='عنوان')),
                ('amount', models.IntegerField(verbose_name='مبلغ')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('description', models.CharField(blank=True, max_length=50, null=True, verbose_name='توضیحات')),
                ('employee_salary', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='salary.employeesalary', verbose_name='employeesalary')),
            ],
            options={
                'verbose_name': 'SalaryLine',
                'verbose_name_plural': 'SalaryLines',
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_entered', models.DateTimeField(blank=True, null=True, verbose_name='ورود')),
                ('date_exited', models.DateTimeField(blank=True, null=True, verbose_name='خروج')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.employee', verbose_name='employee')),
                ('work_day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='salary.workday', verbose_name='work_day')),
            ],
            options={
                'verbose_name': 'Attendance',
                'verbose_name_plural': 'Attendances',
            },
        ),
        migrations.CreateModel(
            name='Vacation',
            fields=[
                ('salarypage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='salary.salarypage')),
                ('vacation_started', models.DateTimeField(verbose_name='vacation_started')),
                ('vacation_ended', models.DateTimeField(blank=True, null=True, verbose_name='vacation_ended')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectmanager.employee', verbose_name='employee')),
            ],
            options={
                'verbose_name': 'Vacation',
                'verbose_name_plural': 'Vacations',
            },
            bases=('salary.salarypage',),
        ),
    ]
