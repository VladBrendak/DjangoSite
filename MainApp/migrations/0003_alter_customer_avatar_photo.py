# Generated by Django 4.0.4 on 2022-06-22 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MainApp', '0002_alter_customer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='avatar_photo',
            field=models.ImageField(default='photos/user_avatar.png', upload_to='photos/'),
        ),
    ]
