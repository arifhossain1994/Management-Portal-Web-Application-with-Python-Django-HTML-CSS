# Generated by Django 2.2.7 on 2019-11-10 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TAmanage', '0002_auto_20191110_1815'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='userType',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.SmallIntegerField(default=1),
        ),
    ]
