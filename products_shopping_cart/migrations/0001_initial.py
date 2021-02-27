# Generated by Django 3.1.4 on 2021-01-20 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.IntegerField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(blank=True, max_length=50, null=True)),
                ('model', models.CharField(blank=True, max_length=50, null=True)),
                ('maker', models.CharField(blank=True, max_length=255, null=True)),
                ('stock', models.IntegerField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created_on')),
            ],
            options={
                'db_table': 'products',
                'managed': True,
            },
        ),
    ]