from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Player(models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    uniform = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(99)]
    )
    position = models.CharField(max_length=16, blank=True, default="")
    height = models.CharField(max_length=6, blank=True, default="")
    hometown = models.CharField(max_length=32, blank=True, default="")
    high_school = models.CharField(max_length=32, blank=True, default="")
    image = models.ImageField(upload_to="static/images/players")
    stats = models.JSONField(default=dict, blank=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        unique_together = ("uniform", "team")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} - {self.team.school.full_name} {self.team.get_sport_display()}"
