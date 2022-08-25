# Generated by Django 3.2 on 2022-05-30 05:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('st', '0008_auto_20220523_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='syusseki_state',
            field=models.CharField(default='☓', max_length=1),
        ),
        migrations.AddField(
            model_name='account',
            name='zaisitu_state',
            field=models.CharField(default='☓', max_length=1),
        ),
        migrations.AlterField(
            model_name='account',
            name='kotei_mac_adress',
            field=models.CharField(max_length=12, validators=[django.core.validators.MinLengthValidator(12), django.core.validators.RegexValidator('^[A-Z0-9]*$')]),
        ),
        migrations.AlterField(
            model_name='account',
            name='private_mac_adress',
            field=models.CharField(max_length=12, validators=[django.core.validators.MinLengthValidator(12), django.core.validators.RegexValidator('^[A-Z0-9]*$')]),
        ),
    ]
