# Generated by Django 3.1.1 on 2020-10-13 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20201005_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='visible',
            field=models.BooleanField(default=False),
        ),
    ]
