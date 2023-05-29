# Generated by Django 3.2 on 2023-05-26 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20230526_2302'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='user',
            name='me_username_constraint',
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, username__iexact='me'), name='me_username_constraint'),
        ),
    ]