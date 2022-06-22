# Generated by Django 3.1.1 on 2021-02-04 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_client_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='pronouns',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('trans', 'Trans'), ('non-binary', 'Non-binary'), ('prefer not to say', 'Prefer not to say'), ('other', 'Other')], max_length=20, null=True),
        ),
    ]
