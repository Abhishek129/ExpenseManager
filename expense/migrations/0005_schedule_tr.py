# Generated by Django 3.2.3 on 2021-06-08 05:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expense', '0004_auto_20210607_1735'),
    ]

    operations = [
        migrations.CreateModel(
            name='schedule_tr',
            fields=[
                ('sc_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('note', models.CharField(max_length=500)),
                ('added_on', models.DateField(default=django.utils.timezone.now)),
                ('time', models.TimeField(auto_now_add=True)),
                ('repeat', models.CharField(max_length=30)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense.category')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]