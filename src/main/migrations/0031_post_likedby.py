# Generated by Django 3.1.5 on 2021-03-28 01:19

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0030_auto_20210327_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='LikedBy',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
