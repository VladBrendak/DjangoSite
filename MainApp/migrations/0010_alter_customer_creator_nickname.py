# Generated by Django 4.1.4 on 2022-12-11 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0009_alter_customer_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='creator_nickname',
            field=models.CharField(blank=True, max_length=35),
        ),
    ]
