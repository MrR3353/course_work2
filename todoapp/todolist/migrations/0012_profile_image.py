# Generated by Django 4.2.6 on 2023-10-14 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0011_alter_profile_is_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='img', upload_to='images'),
            preserve_default=False,
        ),
    ]
