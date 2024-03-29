# Generated by Django 3.2.8 on 2021-10-19 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DjCeleryCrontabSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minute', models.CharField(max_length=64)),
                ('hour', models.CharField(max_length=64)),
                ('day_of_week', models.CharField(max_length=64)),
                ('day_of_month', models.CharField(max_length=64)),
                ('month_of_year', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'djcelery_crontabschedule',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjCeleryIntervalSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('every', models.IntegerField()),
                ('period', models.CharField(max_length=24)),
            ],
            options={
                'db_table': 'djcelery_intervalschedule',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjCeleryPeriodicTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('task', models.CharField(max_length=200)),
                ('args', models.TextField()),
                ('kwargs', models.TextField()),
                ('queue', models.CharField(blank=True, max_length=200, null=True)),
                ('exchange', models.CharField(blank=True, max_length=200, null=True)),
                ('routing_key', models.CharField(blank=True, max_length=200, null=True)),
                ('expires', models.DateTimeField(blank=True, null=True)),
                ('enabled', models.BooleanField()),
                ('last_run_at', models.DateTimeField(blank=True, null=True)),
                ('total_run_count', models.IntegerField()),
                ('date_changed', models.DateTimeField()),
                ('description', models.TextField()),
            ],
            options={
                'db_table': 'djcelery_periodictask',
                'managed': False,
            },
        ),
    ]
