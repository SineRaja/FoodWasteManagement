# Generated by Django 4.0.3 on 2022-09-30 21:47

import FoodRequest.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Address', '0005_alter_address_city_alter_address_country_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.CharField(default=FoodRequest.models.get_id, max_length=36, primary_key=True, serialize=False)),
                ('food_type', models.CharField(max_length=100)),
                ('food_description', models.TextField()),
                ('pickup_date_time', models.DateTimeField()),
                ('request_status', models.CharField(choices=[('OPEN', 'OPEN'), ('COMPLETED', 'COMPLETED'), ('CANCELLED', 'CANCELLED')], default='OPEN', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('accepted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accepted_by', to=settings.AUTH_USER_MODEL, verbose_name='Accepted By')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Address.address', verbose_name='Address')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_by', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
            ],
        ),
    ]
