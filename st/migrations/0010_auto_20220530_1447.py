# Generated by Django 3.2 on 2022-05-30 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('st', '0009_auto_20220530_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='syusseki_state',
            field=models.CharField(max_length=1),
        ),
        migrations.AlterField(
            model_name='account',
            name='zaisitu_state',
            field=models.CharField(max_length=1),
        ),
    ]
