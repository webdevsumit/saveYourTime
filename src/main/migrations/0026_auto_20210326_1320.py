# Generated by Django 3.1.5 on 2021-03-26 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_auto_20210326_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='LastSearcheTag',
            field=models.TextField(default='RENTYUG'),
        ),
    ]