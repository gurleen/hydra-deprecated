from django.db import models
from django.utils.translation import gettext_lazy as _
from showrunner.models.rundown_item import RundownItem
from showrunner.models.team import Team


class Rundown(models.Model):
    class GameType(models.TextChoices):
        TEST = "test", _("Test Event")
        NON_CONF = "non-conf", _("Non-Conference")
        CONF = "conf", _("Conference")
        POSTSEASON = "postseason", _("Post-Season")

    name = models.CharField(max_length=64)
    start_time = models.DateTimeField()
    home_team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="home_team")
    away_team = models.ForeignKey("Team", on_delete=models.CASCADE, related_name="away_team")
    sport = models.CharField(max_length=25, choices=Team.Sports.choices)
    event_type = models.CharField(max_length=16, choices=GameType.choices)


    def __str__(self) -> str:
        return self.name