# Generated by Django 3.0.5 on 2020-06-24 20:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200624_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='blogpostseries',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.BlogPostSeries'),
        ),
    ]
