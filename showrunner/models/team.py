import os
from django.db import models
from django.utils.translation import gettext_lazy as _

from showrunner.models.school import School
from util.get_stats import get_stats_for_team
from util.get_roster import get_roster


class Team(models.Model):
    class Sports(models.TextChoices):
        MENS_BASKETBALL = "mens-basketball", _("Men's Basketball")
        WOMENS_BASKETBALL = "womens-basketball", _("Women's Basketball")

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    sport = models.CharField(max_length=25, choices=Sports.choices)
    stats = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ("school", "sport")

    def __str__(self) -> str:
        return f"{self.school.full_name} {self.get_sport_display()}"

    def fetch_stats(self):
        stats_url = os.path.join(
            self.school.website, "sports", self.sport, "stats", "2021-22"
        )
        self.stats = get_stats_for_team(stats_url)

    def fetch_roster(self):
        roster_url = os.path.join(self.school.website, "sports", self.sport, "roster")
        get_roster(roster_url, self.school.website, self)
