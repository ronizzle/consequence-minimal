# Generated by Django 3.2.3 on 2021-05-31 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consequence', '0003_alter_businessnature_impact_per_employees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='nature_of_business',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='consequence.businessnature'),
        ),
    ]