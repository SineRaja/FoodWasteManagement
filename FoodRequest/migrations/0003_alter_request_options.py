# Generated by Django 4.1.1 on 2022-10-01 13:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FoodRequest', '0002_alter_request_address'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='request',
            options={'ordering': ['created_at']},
        ),
    ]
