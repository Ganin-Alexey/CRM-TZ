# Generated by Django 3.2.8 on 2021-10-24 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20211024_1018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.FloatField(default=0, max_length=0, null=True),
        ),
    ]
