# Generated by Django 3.2.16 on 2023-06-07 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('breach_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='premium_search_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='premium_search_used',
            field=models.IntegerField(default=0),
        ),
    ]
