# Generated by Django 4.1 on 2022-10-28 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_historycalldetail_call_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='token_reset_password',
            field=models.CharField(default=None, max_length=20),
        ),
    ]