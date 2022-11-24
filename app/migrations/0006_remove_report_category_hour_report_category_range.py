# Generated by Django 4.1 on 2022-11-02 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_categoryhour_report_category_hour_report_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='category_hour',
        ),
        migrations.AddField(
            model_name='report',
            name='category_range',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.categoryhour'),
            preserve_default=False,
        ),
    ]