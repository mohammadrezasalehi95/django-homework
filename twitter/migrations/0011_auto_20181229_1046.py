# Generated by Django 2.1.4 on 2018-12-29 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0010_merge_20181229_0337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='default.png', upload_to='media/'),
        ),
    ]