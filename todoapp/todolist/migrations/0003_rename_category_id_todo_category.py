# Generated by Django 4.2.4 on 2023-09-20 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0002_category_todo_category_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='category_id',
            new_name='category',
        ),
    ]
