# Generated by Django 4.0.4 on 2022-06-22 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0003_alter_customer_avatar_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=255),
        ),
    ]
