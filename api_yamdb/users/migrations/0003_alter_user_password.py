# Generated by Django 3.2 on 2023-05-24 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(blank=True, max_length=256, verbose_name='Пароль'),
        ),
    ]
