# Generated by Django 3.2 on 2023-05-24 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(blank=True, max_length=256, verbose_name='Код подтверждения'),
        ),
    ]
