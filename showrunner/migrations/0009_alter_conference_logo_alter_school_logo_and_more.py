# Generated by Django 4.0.4 on 2022-04-20 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("showrunner", "0008_school_website_alter_team_stats"),
    ]

    operations = [
        migrations.AlterField(
            model_name="conference",
            name="logo",
            field=models.ImageField(upload_to="static/images/conferences"),
        ),
        migrations.AlterField(
            model_name="school",
            name="logo",
            field=models.ImageField(null=True, upload_to="static/images/teams"),
        ),
        migrations.AlterUniqueTogether(
            name="team",
            unique_together={("school", "sport")},
        ),
    ]
