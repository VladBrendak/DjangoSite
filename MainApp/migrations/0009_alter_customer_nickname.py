# Generated by Django 4.1.4 on 2022-12-11 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0008_alter_customer_creator_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='nickname',
            field=models.CharField(blank=True, max_length=35),
        ),
    ]