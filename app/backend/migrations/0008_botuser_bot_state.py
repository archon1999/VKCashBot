# Generated by Django 3.2 on 2021-10-16 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_alter_taskmanager_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='botuser',
            name='bot_state',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
