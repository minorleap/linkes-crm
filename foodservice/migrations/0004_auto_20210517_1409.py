# Generated by Django 3.1.1 on 2021-05-17 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodservice', '0003_groupbooking_active'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupbooking',
            options={'ordering': ('-active', 'client__first_name')},
        ),
    ]
