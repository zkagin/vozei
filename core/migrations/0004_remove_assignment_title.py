# Generated by Django 3.1.4 on 2020-12-28 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20201228_1555'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='title',
        ),
    ]
