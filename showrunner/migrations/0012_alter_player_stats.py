# Generated by Django 4.0.4 on 2022-04-20 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showrunner', '0011_player_stats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='stats',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
