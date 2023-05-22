# Generated by Django 4.0.4 on 2022-09-18 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Address', '0003_alter_address_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(choices=[('Visakhapatnam', 'Visakhapatnam'), ('Hyderabad', 'Hyderabad'), ('Vijayawada', 'Vijayawada'), ('Bangalore', 'Bangalore'), ('Hubli', 'Hubli'), ('Gokarna', 'Gokarna'), ('Dandali', 'Dandali'), ('Hampi', 'Hampi'), ('Mysore', 'Mysore'), ('Coorg', 'Coorg'), ('Chikmagalur', 'Chikmagalur'), ('Tambaram', 'Tambaram'), ('Pondicherry', 'Pondicherry'), ('Ooty', 'Ooty'), ('Coonoor', 'Coonoor'), ('Coimbatore', 'Coimbatore'), ('Kodaikanal', 'Kodaikanal'), ('Delhi', 'Delhi'), ('Ernakulam', 'Ernakulam'), ('Trivandram', 'Trivandram'), ('Munnar', 'Munnar'), ('Alleppey', 'Alleppey'), ('North Goa', 'North Goa'), ('South Goa', 'South Goa'), ('Central Goa', 'Central Goa'), ('Udaipur', 'Udaipur'), ('Jaisalmer', 'Jaisalmer'), ('Jodhpur', 'Jodhpur'), ('Kasol', 'Kasol'), ('Manali', 'Manali'), ('Agra', 'Agra'), ('Srinagar', 'Srinagar'), ('Lonavala', 'Lonavala'), ('Kandala', 'Kandala'), ('Thekkady', 'Thekkady'), ('Wayanad', 'Wayanad'), ('Kulu', 'Kulu'), ('Hrishikesh', 'Hrishikesh'), ('Gandikota', 'Gandikota'), ('Warangal', 'Warangal'), ('Gawahati', 'Gawahati'), ('Shillong', 'Shillong'), ('Jowai', 'Jowai'), ('Other', 'Other')], default='Visakhapatnam', max_length=30, verbose_name='City'),
        ),
    ]
