# Generated by Django 3.1.1 on 2020-09-26 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_maintenance'),
    ]

    operations = [
        migrations.AddField(
            model_name='thumbnail',
            name='primary',
            field=models.BooleanField(default=False),
        ),
    ]