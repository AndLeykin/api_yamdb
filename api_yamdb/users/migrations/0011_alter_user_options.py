# Generated by Django 3.2 on 2023-05-27 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user_unique_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('id',), 'verbose_name': 'пользователь', 'verbose_name_plural': 'пользователи'},
        ),
    ]
