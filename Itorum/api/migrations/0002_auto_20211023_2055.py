# Generated by Django 3.2.8 on 2021-10-23 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(verbose_name='Дата и время заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='updated_at',
            field=models.DateTimeField(verbose_name='Дата и время обновления заказа'),
        ),
    ]
