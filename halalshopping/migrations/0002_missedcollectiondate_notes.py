# Generated by Django 3.0.5 on 2020-05-23 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('halalshopping', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='missedcollectiondate',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
