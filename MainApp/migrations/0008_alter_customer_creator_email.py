# Generated by Django 4.1.4 on 2022-12-11 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0007_alter_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='creator_email',
            field=models.EmailField(blank=True, max_length=255),
        ),
    ]
