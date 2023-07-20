# Generated by Django 3.2.16 on 2023-06-05 11:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RedeemCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('is_redeemed', models.BooleanField(default=False)),
                ('code_type', models.CharField(choices=[('5', '5'), ('10', '10'), ('15', '15')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_count', models.IntegerField(default=0)),
                ('search_limit', models.IntegerField(default=3)),
                ('redeem_code', models.CharField(blank=True, max_length=50)),
                ('redeem_code_type', models.CharField(blank=True, max_length=10)),
                ('redeemed_codes', models.ManyToManyField(blank=True, to='breach_app.RedeemCode')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
