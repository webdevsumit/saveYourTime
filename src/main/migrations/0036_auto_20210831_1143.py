# Generated by Django 3.1.5 on 2021-08-31 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_auto_20210423_1231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupmessages',
            name='Messages',
        ),
        migrations.DeleteModel(
            name='Logos',
        ),
        migrations.DeleteModel(
            name='GroupMessages',
        ),
    ]