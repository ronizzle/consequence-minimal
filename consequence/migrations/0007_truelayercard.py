# Generated by Django 3.2.3 on 2021-05-31 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consequence', '0006_rename_account_number_sor_code_truelayeraccount_account_number_sort_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrueLayerCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(max_length=200, null=True)),
                ('tl_account_id', models.CharField(max_length=200, null=True)),
                ('card_type', models.CharField(max_length=200, null=True)),
                ('name_on_card', models.CharField(max_length=200, null=True)),
                ('card_network', models.CharField(max_length=200, null=True)),
                ('partial_card_number', models.CharField(max_length=200, null=True)),
                ('currency', models.CharField(choices=[('GBP', 'GBP'), ('USD', 'USD')], max_length=200, null=True)),
                ('provider_display_name', models.CharField(max_length=200, null=True)),
                ('provider_id', models.CharField(max_length=200, null=True)),
                ('provider_logo_uri', models.CharField(max_length=200, null=True)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='consequence.account')),
            ],
        ),
    ]
