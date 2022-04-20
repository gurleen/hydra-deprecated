from django.db import models


class Conference(models.Model):
    name = models.CharField(max_length=64)
    abbr = models.CharField(max_length=6, blank=True, default="")
    logo = models.ImageField(upload_to="static/images/conferences")

    def __str__(self) -> str:
        return f"{self.name}"