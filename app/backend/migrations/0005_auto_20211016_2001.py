# Generated by Django 3.2 on 2021-10-16 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20211016_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cashlink',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='cashlink',
            name='type',
            field=models.IntegerField(choices=[(1, 'Если выбрано <неважно> или <до 30>'), (2, 'Если выбрано <более 30>'), (3, 'Если не получилось взять займы')], verbose_name='Тип'),
        ),
    ]
