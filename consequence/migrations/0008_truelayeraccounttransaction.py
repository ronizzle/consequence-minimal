# Generated by Django 3.2.3 on 2021-06-01 07:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consequence', '0007_truelayercard'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrueLayerAccountTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200, null=True)),
                ('transaction_type', models.CharField(max_length=200, null=True)),
                ('transaction_category', models.CharField(max_length=200, null=True)),
                ('amount', models.FloatField(null=True)),
                ('currency', models.CharField(choices=[('GBP', 'GBP'), ('USD', 'USD')], max_length=200, null=True)),
                ('provider_transaction_category', models.CharField(max_length=200, null=True)),
                ('running_balance_currency', models.CharField(choices=[('GBP', 'GBP'), ('USD', 'USD')], max_length=200, null=True)),
                ('running_balance_amount', models.FloatField(null=True)),
                ('transaction_id', models.CharField(max_length=200, null=True)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='consequence.account')),
            ],
        ),
    ]
