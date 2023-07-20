# Generated by Django 3.2.16 on 2023-06-06 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('breach_app', '0001_initial'),
        ('admin_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('redeem_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='breach_app.redeemcode')),
            ],
        ),
        migrations.DeleteModel(
            name='RedeemCode',
        ),
    ]