# Generated by Django 5.0.9 on 2024-10-10 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GPS_Monitoring_App', '0002_rastreogps'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado_GPS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=30)),
            ],
        ),
    ]