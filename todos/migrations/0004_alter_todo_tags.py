# Generated by Django 4.1.1 on 2022-10-05 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0003_alter_todo_datetime_todo_alter_todo_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='tags',
            field=models.ManyToManyField(to='todos.tag'),
        ),
    ]