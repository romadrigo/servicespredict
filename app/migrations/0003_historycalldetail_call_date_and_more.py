# Generated by Django 4.1 on 2022-10-27 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_report_filter_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='historycalldetail',
            name='call_date',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='historycalldetail',
            name='call_duration',
            field=models.CharField(default='', max_length=10),
        ),
    ]
