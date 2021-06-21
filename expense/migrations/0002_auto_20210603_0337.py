# Generated by Django 3.2.3 on 2021-06-02 22:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expense', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='money_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense', models.IntegerField()),
                ('budget', models.IntegerField()),
                ('currency', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='transaction_info',
            fields=[
                ('tr_id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
                ('note', models.CharField(max_length=500)),
                ('added_on', models.DateField(default=django.utils.timezone.now)),
                ('category_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense.category')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='user',
        ),
        migrations.AddField(
            model_name='money_info',
            name='tr_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense.transaction_info'),
        ),
        migrations.AddField(
            model_name='money_info',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
