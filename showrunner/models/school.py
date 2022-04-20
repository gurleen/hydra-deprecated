from django.db import models
from colorfield.fields import ColorField

from showrunner.models.conference import Conference


class School(models.Model):
    school_name = models.CharField(max_length=32)
    team_name = models.CharField(max_length=32)
    abbr = models.CharField(max_length=6, blank=True, default="")
    logo = models.ImageField(upload_to="static/images/teams", null=True)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    primary_color = ColorField(default="#FF0000")
    secondary_color = ColorField(default="#FF0000", null=True)
    website = models.URLField(null=True)

    def __str__(self) -> str:
        return f"{self.school_name} {self.team_name}"

    @property
    def full_name(self) -> str:
        return f"{self.school_name} {self.team_name}"