# Generated by Django 3.2 on 2022-05-23 08:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('st', '0007_alter_mac_mac2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='mac_adress',
        ),
        migrations.AddField(
            model_name='account',
            name='kotei_mac_adress',
            field=models.CharField(default='AAAAAAAAAAAA', max_length=12, validators=[django.core.validators.MinLengthValidator(12), django.core.validators.RegexValidator('^[A-Z0-9]*$')]),
        ),
        migrations.AddField(
            model_name='account',
            name='private_mac_adress',
            field=models.CharField(default='AAAAAAAAAAAA', max_length=12, validators=[django.core.validators.MinLengthValidator(12), django.core.validators.RegexValidator('^[A-Z0-9]*$')]),
        ),
    ]
