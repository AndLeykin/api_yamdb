# Generated by Django 3.2 on 2023-05-25 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.TextField(blank=True, verbose_name='Код подтверждения'),
        ),
    ]
