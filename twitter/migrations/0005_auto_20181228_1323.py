# Generated by Django 2.1.4 on 2018-12-28 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0004_merge_20181228_1310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='request',
            old_name='brower',
            new_name='browser',
        ),
    ]
