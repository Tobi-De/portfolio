# Generated by Django 3.1 on 2020-08-22 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_automatic_publish_mail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='automatic_publish_mail',
        ),
    ]