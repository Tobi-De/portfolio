# Generated by Django 3.1 on 2020-09-24 18:17

from django.db import migrations
import markdownx.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=markdownx.models.MarkdownxField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='overview',
            field=markdownx.models.MarkdownxField(),
        ),
        migrations.AlterField(
            model_name='series',
            name='body',
            field=markdownx.models.MarkdownxField(blank=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='overview',
            field=markdownx.models.MarkdownxField(),
        ),
    ]
