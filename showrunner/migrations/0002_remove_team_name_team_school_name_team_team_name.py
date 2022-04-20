# Generated by Django 4.0.4 on 2022-04-19 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("showrunner", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="team",
            name="name",
        ),
        migrations.AddField(
            model_name="team",
            name="school_name",
            field=models.CharField(default="", max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="team",
            name="team_name",
            field=models.CharField(default="", max_length=32),
            preserve_default=False,
        ),
    ]
