# Generated by Django 3.1.1 on 2020-11-06 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodhub', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodhubcollection',
            name='halal',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
