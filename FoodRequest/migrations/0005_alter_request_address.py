# Generated by Django 4.1.1 on 2022-10-02 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Address', '0005_alter_address_city_alter_address_country_and_more'),
        ('FoodRequest', '0004_request_company_name_request_company_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Address.address'),
        ),
    ]