# Generated by Django 3.2.3 on 2021-06-05 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0002_auto_20210603_0337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='money_info',
            name='expense',
        ),
        migrations.RemoveField(
            model_name='money_info',
            name='tr_id',
        ),
    ]
