# Generated by Django 3.0.11 on 2021-04-17 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deliver', '0002_auto_20210417_0957'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
