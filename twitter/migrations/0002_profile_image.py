# Generated by Django 2.1.4 on 2018-12-27 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]