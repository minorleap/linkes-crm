# Generated by Django 3.1.1 on 2020-09-04 14:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_remove_groupsession_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupsession',
            options={'ordering': ('-date',)},
        ),
        migrations.AddField(
            model_name='groupsession',
            name='date',
            field=models.DateField(default=datetime.date(2020, 9, 4)),
            preserve_default=False,
        ),
    ]
