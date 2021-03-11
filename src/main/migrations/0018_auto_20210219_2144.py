# Generated by Django 3.1.5 on 2021-02-19 16:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0017_interestedservice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='User',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
        migrations.DeleteModel(
            name='InterestedService',
        ),
    ]
