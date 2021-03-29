# Generated by Django 3.1.5 on 2021-03-27 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_auto_20210327_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='HasImage',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='Image',
            field=models.ImageField(blank=True, null=True, upload_to='postImages'),
        ),
    ]