# Generated by Django 4.1.13 on 2024-03-04 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_rename_daily_action_steps_returningcitizen_daily_actions'),
    ]

    operations = [
        migrations.AddField(
            model_name='returningcitizen',
            name='mDOC',
            field=models.CharField(default=123456, max_length=6),
            preserve_default=False,
        ),
    ]
