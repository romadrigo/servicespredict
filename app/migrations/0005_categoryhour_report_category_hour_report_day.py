# Generated by Django 4.1 on 2022-11-02 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_customuser_token_reset_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryHour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idd', models.CharField(max_length=2)),
                ('name', models.CharField(max_length=50)),
                ('first', models.CharField(max_length=10)),
                ('second', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='category_hour',
            field=models.CharField(default=None, max_length=2),
        ),
        migrations.AddField(
            model_name='report',
            name='day',
            field=models.CharField(default=None, max_length=1),
        ),
    ]