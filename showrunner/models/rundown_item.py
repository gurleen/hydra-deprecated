from django.db import models
from django.utils.translation import gettext_lazy as _
from ordered_model.models import OrderedModel


class RundownItem(OrderedModel):
    class ItemType(models.TextChoices):
        MARKER = "marker", _("Marker")
        VIDEO = "video", _("Video")
        TALENT = "talent", _("Talent On Camera")
        REPLAY = "replay", _("Replay Melt")
        BREAK = "break", _("Ad Break")
        READ = "read", _("On-Air Read")

    rundown = models.ForeignKey("Rundown", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=64)
    estimated_duration = models.DurationField()
    item_type = models.CharField(max_length=16, choices=ItemType.choices)
    video_cue = models.CharField(max_length=64, blank=True, default="")
    audio_cue = models.CharField(max_length=64, blank=True, default="")
    notes = models.TextField(blank=True)

    order_with_respect_to = "rundown"

    class Meta:
        ordering = ("rundown", "order")

    def __str__(self) -> str:
        return f"{self.get_item_type_display()} - {self.name}"